import json
import os
from test.integration.utils.wait_for_service import wait_for_lambda

import pytest
import requests

LAMBDA_URL = os.environ.get("LAMBDA_URL", "http://lambda:8080")


@pytest.fixture(scope="module", autouse=True)
def ensure_lambda_is_up():
    wait_for_lambda(LAMBDA_URL)


def test_lambda_endpoint():
    payload = {"text": "I am super happy to meet you"}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(LAMBDA_URL, json=payload, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "review_id" in result
    assert "sentiment" in result
    assert "confidence" in result
    assert "text" in result


def test_multiple_lambda_requests():
    texts = ["I love this product!", "This is terrible.", "Neutral statement.", "Absolutely amazing experience!"]
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    for text in texts:
        payload = {"text": text}
        response = requests.post(LAMBDA_URL, json=payload, headers=headers)
        assert response.status_code == 200
        result = response.json()
        assert "review_id" in result
        assert "sentiment" in result
        assert "confidence" in result
        assert "text" in result


def test_invalid_lambda_input():
    payload = {"invalid_key": "This should fail"}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(LAMBDA_URL, json=payload, headers=headers)
    assert response.status_code == 400
    response_body = response.json()
    assert "Invalid input" in response_body
