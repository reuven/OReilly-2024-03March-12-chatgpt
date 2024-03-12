#!/usr/bin/env python3

import os
import requests
from argparse import ArgumentParser
from rich.console import Console
from rich.table import Table

def compare_weather(location1, location2, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    result = {}

    response1 = requests.get(base_url.format(location1, api_key))
    response2 = requests.get(base_url.format(location2, api_key))

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
            "Temperature Difference (°C)": temp_diff,
            "Humidity Difference (%)": humidity_diff,
            "Rain Difference (mm)": rain_diff,
            "Snow Difference (mm)": snow_diff
        }
    else:
        result["Error"] = "Failed to get weather data for one or both locations."

    return result

def display_results(location1, location2, results):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim", width=28)
    table.add_column(location1, justify="right")
    table.add_column(location2, justify="right")
    table.add_column("Difference", justify="right")

    for key, value in results.items():
        if "Difference" in key:
            if value > 0:
                value_str = f"[green]{value:+.2f}[/green]"
            else:
                value_str = f"[red]{value:+.2f}[/red]"
        else:
            value_str = str(value)

        metric, unit = key.rsplit(" ", 1)
        table.add_row(metric, "", "", f"{value_str} {unit}")

    console.print(table)

def main():
    parser = ArgumentParser(description="Compare weather between two locations.")
    parser.add_argument("location1", type=str, help="Current location")
    parser.add_argument("location2", type=str, help="Destination location")
    args = parser.parse_args()

    api_key = os.getenv('OPENWEATHER_API_KEY')
    if not api_key:
        print("Please set the OPENWEATHER_API_KEY environment variable.")
        exit(1)

    weather_comparison = compare_weather(args.location1, args.location2, api_key)
    display_results(args.location1, args.location2, weather_comparison)

if __name__ == '__main__':
    main()
