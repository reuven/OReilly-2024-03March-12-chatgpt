import pytest
import requests_mock
from compare_weather import compare_weather  # Adjust the import based on your actual script name and location

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


# Assuming compare_weather returns a dictionary with an 'Error' key in case of errors

def test_api_error(requests_mock):
    """Test handling of API errors, like network issues or server errors."""
    requests_mock.get(requests_mock.ANY, status_code=500)  # Mocking a 500 Internal Server Error for any URL

    result = compare_weather("Location1", "Location2", "fake_key")
    assert "Error" in result
    assert "Failed to get weather data" in result["Error"]

def test_same_location(requests_mock, api_response1):
    """Test entering the same location twice."""
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather?q=SameLocation&appid=fake_key&units=metric", json=api_response1)

    result = compare_weather("SameLocation", "SameLocation", "fake_key")
    # Depending on your implementation, this could be an error or simply show no differences
    assert result["Differences"]["Temperature Difference (°C)"] == 0
    assert result["Differences"]["Humidity Difference (%)"] == 0

def test_partial_api_failure(requests_mock, api_response1):
    """Test handling when one location is valid and the other is not."""
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather?q=GoodLocation&appid=fake_key&units=metric", json=api_response1)
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather?q=BadLocation&appid=fake_key&units=metric", status_code=404)

    result = compare_weather("GoodLocation", "BadLocation", "fake_key")
    assert "Error" in result
    assert "Failed to get weather data for one or both locations" in result["Error"]

def test_valid_data_handling(requests_mock, api_response1, api_response2):
    """Test handling of valid data for two different locations."""
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather?q=Location1&appid=fake_key&units=metric", json=api_response1)
    requests_mock.get("http://api.openweathermap.org/data/2.5/weather?q=Location2&appid=fake_key&units=metric", json=api_response2)

    result = compare_weather("Location1", "Location2", "fake_key")
    assert "Location1" in result and "Location2" in result
    assert "Differences" in result
    # Ensure differences are calculated correctly
    assert result["Differences"]["Temperature Difference (°C)"] == api_response2['main']['temp'] - api_response1['main']['temp']

# Additional useful tests might include:
# - Handling locations with no precipitation data (to ensure the function doesn't break when 'rain' or 'snow' keys are missing)
# - Edge cases, like very small differences that might be rounded away in display
# - Verifying the structure of the returned dictionary matches expectations (keys exist, values are of expected types)

# Note: Implementing these tests may require you to adjust the fixtures and mocks based on the actual responses and errors from OpenWeatherMap API.



@pytest.fixture
def api_base_url():
    return "http://api.openweathermap.org/data/2.5/weather"

def test_bad_location_name(requests_mock, api_base_url):
    """Test handling of an invalid location name."""
    requests_mock.get(f"{api_base_url}?q=BadLocation&appid=fake_key&units=metric", status_code=404)  # Mocking a 404 response for a bad location

    result = compare_weather("BadLocation", "AnotherBadLocation", "fake_key")
    assert "Error" in result  # Assuming your function includes an "Error" key in the result for errors

def test_api_error(requests_mock, api_base_url):
    """Test handling of API errors, such as network issues."""
    requests_mock.get(f"{api_base_url}?q=Location1&appid=fake_key&units=metric", exc=requests.exceptions.ConnectTimeout)

    result = compare_weather("Location1", "Location2", "fake_key")
    assert "Error" in result  # Assuming your function handles exceptions and includes an "Error" key in the result

def test_same_location(requests_mock, api_base_url, api_response1):
    """Test comparing the same location against itself."""
    requests_mock.get(f"{api_base_url}?q=SameLocation&appid=fake_key&units=metric", json=api_response1)

    result = compare_weather("SameLocation", "SameLocation", "fake_key")
    # Assuming your function handles this case, you might expect differences to be 0
    assert result["Differences"]["Temperature Difference (°C)"] == 0
    assert result["Differences"]["Humidity Difference (%)"] == 0
    # Add more assertions as needed

# Add other tests you think would be useful. For example:
def test_no_precipitation_data(requests_mock, api_base_url, api_response1):
    """Test handling of missing precipitation data."""
    # Modify api_response1 to remove 'rain' and 'snow' keys or set them to None
    modified_response = api_response1.copy()
    modified_response.pop('rain', None)
    modified_response.pop('snow', None)

    requests_mock.get(f"{api_base_url}?q=Location&appid=fake_key&units=metric", json=modified_response)

    result = compare_weather("Location", "AnotherLocation", "fake_key")
    # Assuming your function sets precipitation to 0 if data is missing
    assert result["Location"]["Rain (mm)"] == 0
    assert result["Location"]["Snow (mm)"] == 0
    # Add more assertions as needed
