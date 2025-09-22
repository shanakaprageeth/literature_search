# tests/test_utils.py
import pytest
from unittest.mock import patch
from literature_search.utils import robust_get
import requests

def test_robust_get_success():
    with patch("requests.get") as mock_get:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = robust_get("http://example.com")
        assert response.status_code == 200

def test_robust_get_failure():
    with patch("requests.get") as mock_get:
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = robust_get("http://example.com", max_retries=3)
        assert response is None
