import pytest
import requests_mock
import requests
from site_sizes import fetch_url_size  # Adjust the import based on your actual script name and location

def test_fetch_url_size_with_valid_content(requests_mock):
    test_url = "https://example.com"
    mock_content = "Hello World" * 10  # 100 bytes of content
    requests_mock.get(test_url, text=mock_content)

    size = fetch_url_size(test_url)
    assert size == 100, "The size should be 100 bytes for the mock content"

def test_fetch_url_size_with_error(requests_mock):
    test_url = "https://badurl.com"
    requests_mock.get(test_url, status_code=404)

    result = fetch_url_size(test_url)
    assert "Error" in result, "Expected an error message for a 404 response"

def test_fetch_url_size_with_timeout(requests_mock):
    test_url = "https://timeout.com"
    requests_mock.get(test_url, exc=requests.exceptions.ConnectTimeout)

    result = fetch_url_size(test_url)
    assert "Error" in result, "Expected an error message for a timeout exception"
