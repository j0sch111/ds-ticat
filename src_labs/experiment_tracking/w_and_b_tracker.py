import os
from typing import Any, Dict, Optional

import wandb

from .experiment_tracker import ExperimentTracker


class WandBTracker(ExperimentTracker):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def start_run(
        self,
        project_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        os.environ["WANDB_NOTEBOOK_NAME"] = f"./notebooks/project_explorer.ipynb"

        if self.api_key:
            wandb.login(key=self.api_key)
        else:
            wandb.login()

        wandb.init(project=project_name, name=run_name, tags=tags)

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        wandb.log(metrics, step=step)

    def log_params(self, params: Dict[str, Any]):
        wandb.config.update(params)

    def log_model(self, model: Any, name: str):
        wandb.save(name)

    def log_artifact(self, local_path: str, name: Optional[str] = None):
        artifact = wandb.Artifact(name=name or local_path, type="model")
        artifact.add_file(local_path)
        wandb.log_artifact(artifact)

    def set_tags(self, tags: Dict[str, str]):
        wandb.run.tags += list(tags.keys())

    def finish_run(self):
        wandb.finish()
