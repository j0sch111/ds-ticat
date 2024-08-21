import logging
import os
from typing import Any, Dict, List, Optional

import neptune
from neptune.exceptions import InactiveRunException
from src_labs.experiment_tracking.experiment_tracker import ExperimentTracker

logger = logging.getLogger(__name__)


class NeptuneTracker(ExperimentTracker):
    def __init__(self, api_key: str, project: str):
        self.api_key = api_key
        self.project = project
        self.run = None

    def _convert_tags(self, tags: Optional[Dict[str, str]]) -> Optional[List[str]]:
        if tags is None:
            return None
        return [f"{k}:{v}" for k, v in tags.items()]

    def start_run(
        self,
        project_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        try:
            neptune_tags = self._convert_tags(tags)
            self.run = neptune.init_run(
                project=self.project,
                api_token=self.api_key,
                name=run_name,
                tags=neptune_tags,
                capture_stdout=True,
                capture_stderr=True,
                capture_hardware_metrics=True,
                source_files=["**/*.py"],
                capture_traceback=True,
                fail_on_exception=True,
            )
            logger.info(f"Started Neptune run: {self.run['sys/id'].fetch()}")
        except Exception as e:
            logger.error(f"Failed to start Neptune run: {str(e)}")
            raise

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        if not self.run:
            logger.warning("Run not started. Skipping log_metrics.")
            return
        try:
            for key, value in metrics.items():
                self.run[f"metrics/{key}"].log(value, step=step)
        except Exception as e:
            logger.error(f"Failed to log metrics: {str(e)}")

    def log_params(self, params: Dict[str, Any]):
        if not self.run:
            logger.warning("Run not started. Skipping log_params.")
            return
        try:
            self.run["parameters"] = params
        except Exception as e:
            logger.error(f"Failed to log parameters: {str(e)}")

    def log_model(self, model: Any, name: str):
        if not self.run:
            logger.warning("Run not started. Skipping log_model.")
            return
        try:
            self.run[f"models/{name}"].upload(model)
        except Exception as e:
            logger.error(f"Failed to log model: {str(e)}")

    def log_artifact(self, local_path: str, name: Optional[str] = None):
        if not self.run:
            logger.warning("Run not started. Skipping log_artifact.")
            return
        try:
            self.run[f"artifacts/{name or os.path.basename(local_path)}"].upload(
                local_path
            )
        except Exception as e:
            logger.error(f"Failed to log artifact: {str(e)}")

    def set_tags(self, tags: Dict[str, str]):
        if not self.run:
            logger.warning("Run not started. Skipping set_tags.")
            return
        try:
            neptune_tags = self._convert_tags(tags)
            self.run["sys/tags"].add(neptune_tags)
        except Exception as e:
            logger.error(f"Failed to set tags: {str(e)}")

    def finish_run(self):
        if self.run:
            try:
                run_id = self.run["sys/id"].fetch()
                self.run.stop()
                logger.info(f"Finished Neptune run: {run_id}")
            except InactiveRunException:
                logger.warning(
                    f"Neptune run {self.run['sys/id'].fetch()} was already inactive. Skipping stop operation."
                )
            except Exception as e:
                logger.error(f"Failed to finish Neptune run: {str(e)}")
            finally:
                self.run = None
        else:
            logger.warning("No active Neptune run to finish.")
