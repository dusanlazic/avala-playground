import requests
from typing import Literal


def submit(
    flags: list[str],
) -> list[tuple[Literal["accepted", "rejected", "requeued"], str, str]]:
    """
    Submits a list of flags and returns their status based on the flag checking
    service's response. Returns a list of tuples, where each tuple contains the
    flag's status (accepted, rejected, or requeued), the response message, and
    the original flag.

    Use this when the flag checking service allows submitting multiple flags
    at once (e.g. over HTTP).
    """

    flag_responses = requests.put(
        "http://192.168.0.6:5002/flags",
        json={"flags": flags},
        headers={"X-Team-Token": "your-team-token"},
    ).json()

    status_map = {
        "ACCEPTED": "accepted",
        "DENIED": "rejected",
        "RESUBMIT": "requeue",
        "ERROR": "requeue",
    }

    return [
        (
            status_map[response["status"]],
            response["msg"],
            response["flag"],
        )
        for response in flag_responses
    ]
