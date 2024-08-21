import os
import json
import requests
import threading
import subprocess

class ContainerClientUtils:
    SAGEMAKER_PORT = 8009
    LAMBDA_PORT = 8008
    DOCKER_DIR = "/home/j0sch111/github/ds-ticat/infrastructure/containers"
    QUIET_SERVICES = ["integration-tests"]

    @staticmethod
    def call_lambda_container(text):
        lambda_url = os.environ.get("LAMBDA_URL", f"http://localhost:{ContainerClientUtils.LAMBDA_PORT}")
        payload = {"text": text}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.post(lambda_url, json=payload, headers=headers)
        print("Lambda Container Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()

    @staticmethod
    def call_sagemaker_container(text):
        sagemaker_url = f"http://localhost:{ContainerClientUtils.SAGEMAKER_PORT}/invocations"
        payload = {"text": text}
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.post(sagemaker_url, json=payload, headers=headers)
        print("SageMaker Container Response:")
        print(json.dumps(response.json(), indent=2))
        return response.json()

    @staticmethod
    def filter_output(pipe, quiet_services):
        for line in iter(pipe.readline, b""):
            if not any(service in line.decode() for service in quiet_services):
                print(line.decode().strip())

    @classmethod
    def run_docker_compose(self, docker_dir, quiet_services):
        cmd = ["docker", "compose", "-f", "docker-compose.yml", "up", "--no-color"]
        process = subprocess.Popen(
            cmd, cwd=docker_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        for stream in [process.stdout, process.stderr]:
            threading.Thread(
                target=self.filter_output, args=(stream, quiet_services), daemon=True
            ).start()
        return process

    @classmethod
    def start_model_containers(self):
        return self.run_docker_compose(self.DOCKER_DIR, self.QUIET_SERVICES)
