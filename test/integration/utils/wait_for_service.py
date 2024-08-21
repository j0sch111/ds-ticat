import json
import socket
import time

import pytest
import requests


def wait_for_lambda(url, max_timeout=60, initial_backoff=1, backoff_factor=2):
    """
    Wait for Lambda service to become available using exponential backoff.
    """
    start_time = time.time()
    backoff = initial_backoff

    while time.time() - start_time < max_timeout:
        try:
            print(f"Attempting to connect to Lambda at {url}")
            host = url.split("://")[1].split(":")[0]
            ip = socket.gethostbyname(host)
            print(f"Resolved {host} to IP: {ip}")

            payload = {"text": "Test message"}
            headers = {"Content-Type": "application/json", "Accept": "application/json"}

            response = requests.post(url, json=payload, headers=headers, timeout=5)
            print(f"Connected to Lambda. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
            if response.status_code == 200:
                return
            else:
                print(f"Unexpected status code: {response.status_code}")
        except socket.gaierror as e:
            print(f"Failed to resolve hostname {host}: {str(e)}")
        except requests.RequestException as e:
            print(f"Failed to connect to Lambda: {str(e)}")

        sleep_time = min(backoff, max_timeout - (time.time() - start_time))
        print(f"Waiting for {sleep_time} seconds before next attempt")
        time.sleep(sleep_time)
        backoff = min(backoff * backoff_factor, max_timeout)

    pytest.fail(f"Lambda service at {url} did not become available within {max_timeout} seconds")


def wait_for_sagemaker(url, max_timeout=240, initial_backoff=1, backoff_factor=2):
    """
    Wait for SageMaker service to become available using exponential backoff.
    """
    start_time = time.time()
    backoff = initial_backoff

    while time.time() - start_time < max_timeout:
        try:
            print(f"Attempting to connect to SageMaker at {url}")
            host = url.split("://")[1].split(":")[0]
            ip = socket.gethostbyname(host)
            print(f"Resolved {host} to IP: {ip}")

            payload = {"text": "Test message"}
            headers = {"Content-Type": "application/json", "Accept": "application/json"}

            response = requests.post(f"{url}/invocations", json=payload, headers=headers, timeout=5)
            print(f"Connected to SageMaker. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
            if response.status_code == 200:
                return
            else:
                print(f"Unexpected status code: {response.status_code}")
        except socket.gaierror as e:
            print(f"Failed to resolve hostname {host}: {str(e)}")
        except requests.RequestException as e:
            print(f"Failed to connect to SageMaker: {str(e)}")

        sleep_time = min(backoff, max_timeout - (time.time() - start_time))
        print(f"Waiting for {sleep_time} seconds before next attempt")
        time.sleep(sleep_time)
        backoff = min(backoff * backoff_factor, max_timeout)

    pytest.fail(f"SageMaker service at {url} did not become available within {max_timeout} seconds")
