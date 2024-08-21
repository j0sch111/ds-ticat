import os
from typing import Any, Dict, Optional

from comet_ml import Experiment

from .experiment_tracker import ExperimentTracker


class CometTracker(ExperimentTracker):
    def __init__(
        self,
        api_key: str,
        workspace: Optional[str] = None,
        project_name: Optional[str] = None,
    ):
        os.environ["COMET_HTTP_TIMEOUT"] = "30"
        self.api_key = api_key
        self.workspace = workspace
        self.project_name = project_name
        self.experiment = None

    def start_run(
        self,
        project_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        self.experiment = Experiment(
            api_key=self.api_key,
            project_name=project_name or self.project_name,
            workspace=self.workspace,
        )
        if run_name:
            self.experiment.set_name(run_name)
        if tags:
            self.experiment.add_tags(list(tags.keys()))

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        self.experiment.log_metrics(metrics, step=step)

    def log_params(self, params: Dict[str, Any]):
        self.experiment.log_parameters(params)

    def log_model(self, model: Any, name: str):
        self.experiment.log_model(name, model)

    def log_artifact(self, local_path: str, name: Optional[str] = None):
        self.experiment.log_asset(local_path, file_name=name)

    def set_tags(self, tags: Dict[str, str]):
        self.experiment.add_tags(list(tags.keys()))

    def finish_run(self):
        self.experiment.end()
