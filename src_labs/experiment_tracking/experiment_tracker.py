from abc import ABC, abstractmethod


class ExperimentTracker(ABC):
    @abstractmethod
    def start_run(self, project_name: str, run_name: str = None):
        pass

    @abstractmethod
    def log_metrics(self, metrics: dict):
        pass

    @abstractmethod
    def log_model(self, model, name: str):
        pass

    @abstractmethod
    def finish_run(self):
        pass
