from typing import Any
import time
import requests


def fetch() -> dict:
    """
    Fetches raw flag IDs from the game server and returns them as a dictionary.
    Exceptions and retries are handled internally by Avala. It's advisable to
    set a timeout for requests to prevent the server from hanging indefinitely.
    """

    response = requests.get("http://192.168.0.6:5001/teams.json", timeout=10)
    return response.json()


def process(raw: dict) -> dict[str, dict[str, list[Any]]]:
    """
    Processes the raw flag IDs returned by fetch function into a standardized,
    structured format. Flag IDs must be organized by service name and team IP
    address, and be stored in a list where each item corresponds to the flag
    IDs of a single tick.

    Example of the returned dictionary:
    {
        "SomeService": {
            "10.10.24.5": [
                "foo",   # Flag IDs of the most recent tick
                "bar",   # Flag IDs of the previous tick
                (...)
            ],
            (...)
        },
        (...)
    }

    Use type hints as a guide for the expected data structure.
    """

    processed: dict[str, dict[str, list[Any]]] = {}

    for service_name, teams in raw["flag_ids"].items():
        processed[service_name] = {}
        for team_num, flag_ids in teams.items():
            team_ip = f"10.10.{team_num}.1"
            processed[service_name][team_ip] = flag_ids

    return processed
