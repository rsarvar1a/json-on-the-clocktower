import json
import requests


def fetch_remote_data(url: str):
    """Fetch data from a remote URL."""

    response = requests.get(url, timeout=10, allow_redirects=True)
    response.raise_for_status()
    return response.json()


def load_data(filename: str):
    """Load data from a JSON file."""
    with open(filename, encoding="utf-8") as fhandle:
        data = json.load(fhandle)
    return data
