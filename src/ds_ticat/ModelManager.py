import json
import os
import random
import warnings

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss
from sklearn.exceptions import UndefinedMetricWarning
from sklearn.preprocessing import StandardScaler


class ModelManager:
    def __init__(
        self,
        project_root="./",
        model_dir=None,
        data_dir=None,
        model_filename="sentiment_model.joblib",
        data_filename="training_data.jsonl",
        experiment_tracker=None,
    ):
        self.project_root = project_root
        self.model_dir = model_dir if model_dir else os.path.join(project_root, "models")
        self.data_dir = data_dir if data_dir else os.path.join(project_root, "data")
        self.model_path = os.path.join(self.model_dir, model_filename)
        self.data_path = os.path.join(self.data_dir, data_filename)
        self.model = None
        self.experiment_tracker = experiment_tracker

    def validate_setup(self):
        print("Validating project setup...")
        for directory in [self.model_dir, self.data_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            else:
                print(f"Directory exists: {directory}")

        if not os.path.exists(self.data_path):
            print(f"Data file does not exist: {self.data_path}")
            print("Please create a sample data file with at least 50 rows.")
        else:
            print(f"Data file exists: {self.data_path}")

    def train(self, num_iterations=1000):
        print("Training model...")
        X, y = self._load_training_data()

        # Print class distribution
        unique, counts = np.unique(y, return_counts=True)
        print("Class distribution:", dict(zip(unique, counts)))

        X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.25, random_state=42)

        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
            ('scaler', StandardScaler(with_mean=False)),
            ('clf', SGDClassifier(loss='log_loss', alpha=0.0001, max_iter=1000, tol=1e-3, random_state=42))
        ])

        # Initial fit
        self.model.fit(X_train, y_train)

        for i in range(num_iterations):
            # Use partial_fit for online learning
            self.model.named_steps['clf'].partial_fit(
                self.model.named_steps['tfidf'].transform(X_train),
                y_train,
                classes=np.unique(y)
            )

            # Calculate and log metrics
            train_pred = self.model.predict(X_train)
            val_pred = self.model.predict(X_val)
            train_prob = self.model.predict_proba(X_train)
            val_prob = self.model.predict_proba(X_val)

            train_accuracy = accuracy_score(y_train, train_pred)
            val_accuracy = accuracy_score(y_val, val_pred)

            epsilon = 1e-15
            train_loss = log_loss(y_train, np.clip(train_prob, epsilon, 1 - epsilon))
            val_loss = log_loss(y_val, np.clip(val_prob, epsilon, 1 - epsilon))

            if self.experiment_tracker:
                metrics = {
                    'iteration': i + 1,
                    'train_samples': len(X_train),
                    'train_accuracy': train_accuracy,
                    'val_accuracy': val_accuracy,
                    'train_loss': train_loss,
                    'val_loss': val_loss,
                    'train_precision': precision_score(y_train, train_pred, average='weighted', zero_division=0),
                    'val_precision': precision_score(y_val, val_pred, average='weighted', zero_division=0),
                    'train_recall': recall_score(y_train, train_pred, average='weighted', zero_division=0),
                    'val_recall': recall_score(y_val, val_pred, average='weighted', zero_division=0),
                    'train_f1': f1_score(y_train, train_pred, average='weighted', zero_division=0),
                    'val_f1': f1_score(y_val, val_pred, average='weighted', zero_division=0),
                }
                self.experiment_tracker.log_metrics(metrics, step=i)

            # Print progress
            if i % 100 == 0:
                print(f"Iteration {i}: Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")

        # Final evaluation on test set
        y_test_pred = self.model.predict(X_test)
        test_accuracy = accuracy_score(y_test, y_test_pred)
        test_precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
        test_recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
        test_f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)

        if self.experiment_tracker:
            final_metrics = {
                'test_accuracy': test_accuracy,
                'test_precision': test_precision,
                'test_recall': test_recall,
                'test_f1': test_f1
            }
            self.experiment_tracker.log_metrics(final_metrics)

        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")

        if self.experiment_tracker:
            self.experiment_tracker.log_model(self.model_path, "sentiment_model.joblib")
            self.experiment_tracker.finish_run()

    def _load_training_data(self):
        texts = []
        labels = []
        with open(self.data_path, 'r') as f:
            for line in f:
                example = json.loads(line)
                texts.append(example['text'])
                labels.append(example['label'])
        return texts, labels


    def predict(self, text):
        if self.model is None:
            self.load_model()

        prediction = self.model.predict([text])[0]
        probability = np.max(self.model.predict_proba([text]))
        return prediction, probability

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError(f"No model found at {self.model_path}. Please train the model first.")

    def get_project_info(self):
        return {
            "project_root": self.project_root,
            "model_directory": self.model_dir,
            "data_directory": self.data_dir,
            "model_path": self.model_path,
            "data_path": self.data_path,
        }
