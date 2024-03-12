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

        # Individual weather details
        weather_details1 = {
            "Temperature (°C)": weather1['main']['temp'],
            "Humidity (%)": weather1['main']['humidity'],
            "Rain (mm)": weather1['rain']['1h'] if 'rain' in weather1 else 0,
            "Snow (mm)": weather1['snow']['1h'] if 'snow' in weather1 else 0
        }

        weather_details2 = {
            "Temperature (°C)": weather2['main']['temp'],
            "Humidity (%)": weather2['main']['humidity'],
            "Rain (mm)": weather2['rain']['1h'] if 'rain' in weather2 else 0,
            "Snow (mm)": weather2['snow']['1h'] if 'snow' in weather2 else 0
        }

        # Differences
        result['Differences'] = {
            "Temperature Difference (°C)": weather2['main']['temp'] - weather1['main']['temp'],
            "Humidity Difference (%)": weather2['main']['humidity'] - weather1['main']['humidity'],
            "Rain Difference (mm)": weather_details2["Rain (mm)"] - weather_details1["Rain (mm)"],
            "Snow Difference (mm)": weather_details2["Snow (mm)"] - weather_details1["Snow (mm)"]
        }

        result[location1] = weather_details1
        result[location2] = weather_details2

    else:
        result["Error"] = "Failed to get weather data for one or both locations."

    return result

def display_results(locations, results):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim", width=28)

    for location in locations:
        table.add_column(location, justify="right")

    table.add_column("Difference", justify="right")

    # Adding weather details for each location
    for metric in results[locations[0]].keys():
        row = [metric]
        for location in locations:
            value = results[location][metric]
            row.append(f"{value:.2f}" if isinstance(value, float) else str(value))

        # Difference (only for temperature and humidity)
        if "Difference" in metric:
            diff = results['Differences'][metric]
            diff_str = f"[green]{diff:+.2f}[/green]" if diff > 0 else f"[red]{diff:+.2f}[/red]"
            row.append(diff_str)
        else:
            row.append("")

        table.add_row(*row)

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
    display_results([args.location1, args.location2], weather_comparison)

if __name__ == '__main__':
    main()
