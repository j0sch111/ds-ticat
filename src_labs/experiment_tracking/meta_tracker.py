import importlib
import logging
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from .credentials_helper import CredentialLocation, CredentialsHelper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TrackerType(Enum):
    W_AND_B = auto()
    MLFLOW = auto()
    NEPTUNE = auto()
    COMET = auto()


class TrackerConfig:
    def __init__(self, tracker_type: TrackerType, **kwargs):
        self.tracker_type = tracker_type
        self.config = kwargs


class MetaTracker:
    def __init__(self, tracker_configs: List[TrackerConfig]):
        self.tracker_configs = tracker_configs
        self.trackers = []
        self.active_trackers = []

    def _initialize_trackers(self):
        for config in self.tracker_configs:
            try:
                tracker = MetaTrackerFactory.create_tracker(config)
                self.trackers.append(tracker)
            except Exception as e:
                print(
                    f"Failed to initialize tracker for {config.tracker_type}: {str(e)}"
                )

    def start_run(
        self,
        project_name: str,
        run_name: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
    ):
        if not self.trackers:
            self._initialize_trackers()

        self.active_trackers = []
        for tracker in self.trackers:
            try:
                tracker.start_run(project_name, run_name, tags)
                self.active_trackers.append(tracker)
            except Exception as e:
                print(f"Failed to start run for {tracker.__class__.__name__}: {str(e)}")

    def log_metrics(self, metrics: Dict[str, float], step: Optional[int] = None):
        for tracker in self.active_trackers:
            try:
                tracker.log_metrics(metrics, step)
            except Exception as e:
                logger.error(
                    f"Failed to log metrics for {tracker.__class__.__name__}: {str(e)}"
                )

    def log_params(self, params: Dict[str, Any]):
        for tracker in self.active_trackers:
            try:
                tracker.log_params(params)
            except Exception as e:
                logger.error(
                    f"Failed to log params for {tracker.__class__.__name__}: {str(e)}"
                )

    def log_model(self, model: Any, name: str):
        for tracker in self.active_trackers:
            try:
                tracker.log_model(model, name)
            except Exception as e:
                logger.error(
                    f"Failed to log model for {tracker.__class__.__name__}: {str(e)}"
                )

    def log_artifact(self, local_path: str, name: Optional[str] = None):
        for tracker in self.active_trackers:
            try:
                tracker.log_artifact(local_path, name)
            except Exception as e:
                logger.error(
                    f"Failed to log artifact for {tracker.__class__.__name__}: {str(e)}"
                )

    def set_tags(self, tags: Dict[str, str]):
        for tracker in self.active_trackers:
            try:
                tracker.set_tags(tags)
            except Exception as e:
                logger.error(
                    f"Failed to set tags for {tracker.__class__.__name__}: {str(e)}"
                )

    def finish_run(self):
        for tracker in self.active_trackers:
            try:
                tracker.finish_run()
            except Exception as e:
                logger.error(
                    f"Failed to finish run for {tracker.__class__.__name__}: {str(e)}"
                )
        self.active_trackers = []

    @staticmethod
    def generate_unique_experiment_name(base_name="experiment"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_string = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=6)
        )
        return f"{base_name}_{timestamp}_{random_string}"


class MetaTrackerFactory:
    @staticmethod
    def _import_tracker(tracker_type: TrackerType):
        tracker_info = {
            TrackerType.W_AND_B: ("w_and_b_tracker", "WandBTracker"),
            TrackerType.MLFLOW: ("mlflow_tracker", "MLFlowTracker"),
            TrackerType.NEPTUNE: ("neptune_tracker", "NeptuneTracker"),
            TrackerType.COMET: ("comet_tracker", "CometTracker"),
        }

        module_name, class_name = tracker_info.get(tracker_type, (None, None))
        if module_name is None or class_name is None:
            raise ValueError(f"Unknown tracker type: {tracker_type}")

        module = importlib.import_module(f".{module_name}", package=__package__)
        return getattr(module, class_name)

    @staticmethod
    def create_tracker(tracker_config: TrackerConfig):
        tracker_class = MetaTrackerFactory._import_tracker(tracker_config.tracker_type)

        if tracker_config.tracker_type == TrackerType.W_AND_B:
            return tracker_class(
                api_key=CredentialsHelper.get_credential(CredentialLocation.WANDB)
            )
        elif tracker_config.tracker_type == TrackerType.COMET:
            return tracker_class(
                api_key=CredentialsHelper.get_credential(CredentialLocation.COMET),
                workspace=tracker_config.config.get("workspace"),
                project_name=tracker_config.config.get("project_name"),
            )
        elif tracker_config.tracker_type == TrackerType.MLFLOW:
            return tracker_class(
                tracking_uri=tracker_config.config.get(
                    "tracking_uri", "http://localhost:5000"
                )
            )
        elif tracker_config.tracker_type == TrackerType.NEPTUNE:
            return tracker_class(
                api_key=CredentialsHelper.get_credential(CredentialLocation.NEPTUNE),
                project=tracker_config.config.get("project"),
            )
        else:
            raise ValueError(f"Unsupported tracker type: {tracker_config.tracker_type}")

    @staticmethod
    def create_meta_tracker(configs: List[TrackerConfig]) -> MetaTracker:
        return MetaTracker(configs)
