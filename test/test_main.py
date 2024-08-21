from src.ds_ticat.ModelManager import ModelManager
import unittest
import os
import tempfile
import shutil

class TestModelManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.model_manager = ModelManager(project_root=self.test_dir)

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_init(self):
        # Test if ModelManager initializes correctly
        self.assertEqual(self.model_manager.project_root, self.test_dir)
        self.assertEqual(self.model_manager.model_dir, os.path.join(self.test_dir, "models"))
        self.assertEqual(self.model_manager.data_dir, os.path.join(self.test_dir, "data"))

    def test_validate_setup(self):
        # Test if validate_setup creates necessary directories
        self.model_manager.validate_setup()
        self.assertTrue(os.path.exists(self.model_manager.model_dir))
        self.assertTrue(os.path.exists(self.model_manager.data_dir))
        self.assertTrue(os.path.exists(self.model_manager.data_path))

    def test_train_and_predict(self):
        # Test if we can train a model and make predictions
        self.model_manager.validate_setup()
        self.model_manager.train()
        self.assertTrue(os.path.exists(self.model_manager.model_path))

        # Test prediction
        prediction, probability = self.model_manager.predict("This is a great product!")
        self.assertIn(prediction, ["POSITIVE", "NEGATIVE"])
        self.assertTrue(0 <= probability <= 1)

if __name__ == '__main__':
    unittest.main()
