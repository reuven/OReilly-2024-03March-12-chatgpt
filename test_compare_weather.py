import pytest
import requests_mock
from your_script_name import compare_weather, display_results  # Adjust the import based on your actual script name and location

@pytest.fixture
def api_response1():
    """Mock API response for location1."""
    return {
        "main": {
            "temp": 20,
            "humidity": 50,
        },
        "rain": {"1h": 2},
        "snow": {"1h": 0}
    }

@pytest.fixture
def api_response2():
    """Mock API response for location2."""
    return {
        "main": {
            "temp": 25,
            "humidity": 60,
        },
        "rain": {"1h": 0},
        "snow": {"1h": 1}
    }

def test_compare_weather(requests_mock, api_response1, api_response2):
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather?q=Location1&appid=fake_key&units=metric", json=api_response1)
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather?q=Location2&appid=fake_key&units=metric", json=api_response2)

    results = compare_weather("Location1", "Location2", "fake_key")
    assert results["Location1"]["Temperature (°C)"] == 20
    assert results["Location2"]["Temperature (°C)"] == 25
    assert results["Differences"]["Temperature Difference (°C)"] == 5
    # Add more assertions based on your function's return structure

# Test for display_results might not be straightforward due to its nature of printing to the console
# Instead, you could test individual components that contribute to what it displays, like data processing functions

# Note: It's challenging to write a conventional test for `display_results` since it primarily deals with console output.
# You might consider using the `capsys` fixture to capture print outputs if needed, but this can get complex with rich library outputs.
