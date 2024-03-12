#!/usr/bin/env python3

import requests
from argparse import ArgumentParser
from rich import Console, Table

def fetch_url_size(url):
    """Fetches the content length of the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        size = len(response.content)
        return size
    except requests.RequestException as e:
        return f"Error: {e}"

def main():
    parser = ArgumentParser(description="Fetch and print the content sizes of given URLs.")
    parser.add_argument('urls', nargs='+', help='One or more URLs to fetch')
    args = parser.parse_args()

    console = Console()
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("URL", style="dim", width=50)
    table.add_column("Size / Error")

    for url in args.urls:
        size = fetch_url_size(url)
        if isinstance(size, int):
            # Format the size with commas
            size_formatted = f"{size:,} bytes"
        else:
            size_formatted = size  # Error message

        table.add_row(url, size_formatted)

    console.print(table)

if __name__ == '__main__':
    main()
