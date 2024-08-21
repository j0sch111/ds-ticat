import json
import os
from test.integration.utils.wait_for_service import wait_for_sagemaker

import pytest
import requests

SAGEMAKER_URL = os.environ.get("SAGEMAKER_URL", "http://sagemaker:8080")


@pytest.fixture(scope="module", autouse=True)
def ensure_sagemaker_is_up():
    wait_for_sagemaker(SAGEMAKER_URL)


def test_sagemaker_endpoint():
    payload = {"text": "I am super happy to meet you"}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(f"{SAGEMAKER_URL}/invocations", json=payload, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "label" in result
    assert "confidence" in result
    assert "model_id" in result


def test_multiple_sagemaker_requests():
    texts = ["I love this product!", "This is terrible.", "Neutral statement.", "Absolutely amazing experience!"]
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    for text in texts:
        payload = {"text": text}
        response = requests.post(f"{SAGEMAKER_URL}/invocations", json=payload, headers=headers)
        assert response.status_code == 200
        result = response.json()
        assert "label" in result
        assert "confidence" in result
        assert "model_id" in result


def test_invalid_sagemaker_input():
    payload = {"invalid_key": "This should fail"}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(f"{SAGEMAKER_URL}/invocations", json=payload, headers=headers)
    assert response.status_code == 500  # The current behavior returns 500 for invalid input
    assert "Input data should be a string or a dictionary with 'text' key" in response.text
