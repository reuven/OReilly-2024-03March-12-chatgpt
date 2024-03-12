#!/usr/bin/env python3

import argparse
import os
import requests

def compare_weather(location1, location2, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

    response1 = requests.get(base_url.format(location1, api_key))
    response2 = requests.get(base_url.format(location2, api_key))
    result = {}

    if response1.status_code == 200 and response2.status_code == 200:
        weather1 = response1.json()
        weather2 = response2.json()

        temp_diff = weather2['main']['temp'] - weather1['main']['temp']
        humidity_diff = weather2['main']['humidity'] - weather1['main']['humidity']

        precipitation1 = {"rain": 0, "snow": 0}
        precipitation2 = {"rain": 0, "snow": 0}

        if 'rain' in weather1:
            precipitation1['rain'] = weather1['rain'].get('1h', 0)
        if 'rain' in weather2:
            precipitation2['rain'] = weather2['rain'].get('1h', 0)

        if 'snow' in weather1:
            precipitation1['snow'] = weather1['snow'].get('1h', 0)
        if 'snow' in weather2:
            precipitation2['snow'] = weather2['snow'].get('1h', 0)

        rain_diff = precipitation2['rain'] - precipitation1['rain']
        snow_diff = precipitation2['snow'] - precipitation1['snow']

        result = {
            "Temperature Difference": f"{temp_diff:.2f}°C",
            "Humidity Difference": f"{humidity_diff}%",
            "Rain Difference": f"{rain_diff}mm",
            "Snow Difference": f"{snow_diff}mm"
        }
    else:
        result["Error"] = "Failed to get weather data for one or both locations."

    return result

def main():
    parser = argparse.ArgumentParser(description="Compare weather between two locations.")
    parser.add_argument("current_location", help="Your current location")
    parser.add_argument("destination_location", help="Your destination location")

    args = parser.parse_args()

    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("Please set the OPENWEATHER_API_KEY environment variable.")
        exit(1)

    weather_comparison = compare_weather(args.current_location,
                                         args.destination_location,
                                         api_key)
    for key, value in weather_comparison.items():
        print(f"{key}: {value}")

if __name__ == '__main__':
    main()
