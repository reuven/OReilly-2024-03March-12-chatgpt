import pytest
import requests_mock
from compare_weather import compare_weather  # Adjust the import based on your actual script name and location

# Assuming compare_weather returns a dictionary with an 'Error' key in case of errors

def test_bad_location_name(requests_mock):
    """Test handling of an invalid location name."""
    requests_mock.get(requests_mock.ANY, status_code=404)  # Mocking a 404 response for any URL

    result = compare_weather("BadLocation1", "BadLocation2", "fake_key")
    assert "Error" in result
    assert "Failed to get weather data" in result["Error"]

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
