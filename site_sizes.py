#!/usr/bin/env python3

import requests
from argparse import ArgumentParser

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

    for url in args.urls:
        size = fetch_url_size(url)
        print(f"{url}: {size} bytes")

if __name__ == '__main__':
    main()
