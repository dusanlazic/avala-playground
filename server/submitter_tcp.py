from pwn import *
from typing import Literal


def setup():
    """
    Gets called before the Avala server starts accepting flags. Use it to
    establish a TCP connection to the flag submitting service, initiate a
    session, etc.

    Object returned from this function will be passed as the second argument
    to the submit function.
    """

    r = remote("192.168.0.6", 5003)
    r.recvuntil(b"\n\n")
    return r


def submit(flag: str, r) -> tuple[Literal["accepted", "rejected", "requeued"], str]:
    """
    Submits a single flag to the flag checking service. Returns a tuple
    containing the flag's status (accepted, rejected, or requeued)
    and the response message from the service.

    Use this when the flag checking service allows submitting only one flag
    at the time (e.g. over TCP).
    """

    r.sendline(flag.encode())

    response = r.recvline().decode().strip()

    if response.endswith("OK"):
        return "accepted", response
    else:
        return "rejected", response


def teardown(r):
    """
    Gets called during the shutdown process to clean up any resources,
    such as closing the connection and similar.
    """

    r.close()
