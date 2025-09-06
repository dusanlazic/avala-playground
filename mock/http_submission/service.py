import os
import random
import re
from typing import Dict, List

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI()

FLAG_PATTERN = re.compile(os.getenv("FLAG_PATTERN", r"^[A-Z0-9]{31}=$"))

RESPONSES = [
    "ACCEPTED: flag claimed",
    "DENIED: invalid flag",
    "DENIED: flag from nop team",
    "DENIED: flag is your own",
    "DENIED: flag too old",
    "DENIED: flag already claimed",
    "RESUBMIT: the flag is not active yet, wait for next round",
    "ERROR: notify the organizers and retry later",
]


class FlagSubmission(BaseModel):
    flags: List[str]


@app.put("/flags")
async def submit_flags(
    flags: FlagSubmission, x_team_token: str = Header(...)
) -> List[Dict[str, str]]:
    if not x_team_token:
        raise HTTPException(status_code=400, detail="X-Team-Token header is required")

    responses = []

    for flag in flags.flags:
        if not FLAG_PATTERN.match(flag):
            responses.append(
                {
                    "msg": f"[{flag}] DENIED: invalid flag",
                    "flag": flag,
                    "status": "DENIED",
                }
            )
        else:
            if random.random() < 0.9:
                message = "ACCEPTED: flag claimed"
                status = "ACCEPTED"
            else:
                message = random.choice(RESPONSES[1:])
                status = (
                    "DENIED"
                    if "DENIED" in message
                    else "RESUBMIT"
                    if "RESUBMIT" in message
                    else "ERROR"
                )

            responses.append(
                {"msg": f"[{flag}] {message}", "flag": flag, "status": status}
            )

    return responses
