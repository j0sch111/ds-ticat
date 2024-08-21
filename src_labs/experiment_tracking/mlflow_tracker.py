import logging
from typing import Any, Dict, Optional
from urllib.parse import urlparse, urlunparse

import mlflow
from mlflow.tracking import MlflowClient

from .experiment_tracker import ExperimentTracker

logger = logging.getLogger(__name__)


class MLFlowTracker(ExperimentTracker):
    def __init__(self, tracking_uri: Optional[str] = None):
        self.tracking_uri = self._validate_and_correct_url(
            tracking_uri or "http://localhost:5000"
        )
        self.client = None
        self.run = None

    def _validate_and_correct_url(self, url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme:
            # If no scheme is provided, assume http
            url = "http://" + url
            parsed = urlparse(url)

        if parsed.scheme not in ["http", "https"]:
            raise ValueError(
                f"Invalid URL scheme: {parsed.scheme}. Must be http or https."
            )

        # Ensure there's a netloc (domain)
        if not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}. Missing domain.")

        # Reconstruct the URL to ensure it's properly formatted
        return urlunparse(parsed)

    def _ensure_client(self):
        if self.client is None:
            try:
                mlflow.set_tracking_uri(self.tracking_uri)
                self.client = MlflowClient(tracking_uri=self.tracking_uri)
                logger.info(
                    f"MLflow client created with tracking URI: {self.tracking_uri}"
                )
            except Exception as e:
                logger.error(f"Failed to create MLflow client: {str(e)}")
                raise

    def start_run(
        self,
        project_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        self._ensure_client()
        try:
            experiment = self.client.get_experiment_by_name(project_name)
            if experiment is None:
                experiment_id = self.client.create_experiment(project_name)
            else:
                experiment_id = experiment.experiment_id
            self.run = self.client.create_run(
                experiment_id, run_name=run_name, tags=tags
            )
            logger.info(f"Started MLflow run: {self.run.info.run_id}")
        except Exception as e:
            logger.error(f"Failed to start MLflow run: {str(e)}")
            raise

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        if not self.run:
            logger.error("MLflow run not started. Call start_run() first.")
            raise Exception("Run not started. Call start_run() first.")
        try:
            for key, value in metrics.items():
                self.client.log_metric(self.run.info.run_id, key, value, step=step)
        except Exception as e:
            logger.error(f"Failed to log metrics: {str(e)}")
            raise

    def log_params(self, params: Dict[str, Any]):
        if not self.run:
            raise Exception("Run not started. Call start_run() first.")
        for key, value in params.items():
            self.client.log_param(self.run.info.run_id, key, value)

    def log_model(self, model: Any, name: str):
        if not self.run:
            raise Exception("Run not started. Call start_run() first.")
        with mlflow.start_run(run_id=self.run.info.run_id):
            mlflow.sklearn.log_model(model, name)

    def log_artifact(self, local_path: str, name: Optional[str] = None):
        if not self.run:
            raise Exception("Run not started. Call start_run() first.")
        self.client.log_artifact(self.run.info.run_id, local_path, artifact_path=name)

    def set_tags(self, tags: Dict[str, str]):
        if not self.run:
            raise Exception("Run not started. Call start_run() first.")
        for key, value in tags.items():
            self.client.set_tag(self.run.info.run_id, key, value)

    def finish_run(self):
        if self.run:
            try:
                self.client.set_terminated(self.run.info.run_id)
                logger.info(f"Finished MLflow run: {self.run.info.run_id}")
                self.run = None
            except Exception as e:
                logger.error(f"Failed to finish MLflow run: {str(e)}")
                raise
