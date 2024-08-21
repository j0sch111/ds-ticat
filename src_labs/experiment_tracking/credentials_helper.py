import logging
import subprocess
from enum import Enum


class CredentialLocation(Enum):
    WANDB = "Weights_and_Biases_demo"
    MLFLOW = "MLflow_demo"
    NEPTUNE = "Neptune_AI_demo"
    COMET = "Comet_AI_demo"


class CredentialsHelper:

    logging.basicConfig(level=logging.DEBUG)

    @staticmethod
    def get_credential(
        location: CredentialLocation, field: str = "Anmeldedaten"
    ) -> str:
        logging.info("Requesting credentials from OnePassword")

        try:
            result = subprocess.run(
                ["op", "item", "get", location.value, "--fields", field],
                capture_output=True,
                text=True,
                check=True,
            )

            logging.info("Successfully recieved credentials")

            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to retrieve credential for {location.name}: {e}")
