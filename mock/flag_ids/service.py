import hashlib
import json
import os
import random
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from faker import Faker
from fastapi import FastAPI

FIRST_TICK_START = datetime.fromisoformat(
    os.getenv("FIRST_TICK_START", "2025-04-21T00:00:00")
).replace(tzinfo=ZoneInfo(os.getenv("TZ", "Europe/Belgrade")))
TICK_DURATION = timedelta(seconds=int(os.getenv("TICK_DURATION", "60")))
SEED = 1337

app = FastAPI()


@app.get("/teams.json")
def get_flag_ids():
    team_numbers = generate_team_numbers(SEED)
    services = generate_service_names(SEED)
    current_tick = get_current_tick()
    recent_ticks = range(current_tick, max(current_tick - 4, 1) - 1, -1)

    print(recent_ticks)

    generators = [
        generate_username,
        generate_email,
        generate_chrome_agent,
        generate_uuid,
        generate_uri_path,
        generate_domain_and_ipv4,
        generate_file_path,
    ]

    random.seed(SEED)
    random.shuffle(generators)

    flag_ids = {
        service: {
            str(team): [generators[i](service, team, tick) for tick in recent_ticks]
            for team in team_numbers
        }
        for i, service in enumerate(services)
    }

    return {
        "teams": team_numbers,
        "flag_ids": flag_ids,
    }


def generate_team_numbers(seed: int, count: int = 35) -> list[int]:
    random.seed(seed)
    return [1] + sorted(random.sample(range(1, 255), count))


def generate_service_names(seed: int, count: int = 7) -> list[str]:
    faker = Faker()
    Faker.seed(seed)
    return [faker.word() for _ in range(count)]


def _get_deterministic_faker(service: str, team: int, tick: int) -> Faker:
    seed_input = f"{service}:{team}:{tick}"
    seed = int(hashlib.sha256(seed_input.encode()).hexdigest(), 16) % (10**8)
    faker = Faker()
    faker.seed_instance(seed)
    return faker


def generate_username(service: str, team: int, tick: int) -> str:
    return _get_deterministic_faker(service, team, tick).user_name()


def generate_email(service: str, team: int, tick: int) -> str:
    return _get_deterministic_faker(service, team, tick).email()


def generate_chrome_agent(service: str, team: int, tick: int) -> str:
    return _get_deterministic_faker(service, team, tick).chrome()


def generate_uuid(service: str, team: int, tick: int) -> str:
    return _get_deterministic_faker(service, team, tick).uuid4()


def generate_uri_path(service: str, team: int, tick: int) -> str:
    return _get_deterministic_faker(service, team, tick).uri_path()


def generate_ipv4(service: str, team: int, tick: int) -> str:
    return _get_deterministic_faker(service, team, tick).ipv4()


def generate_file_path(service: str, team: int, tick: int) -> str:
    return _get_deterministic_faker(service, team, tick).file_path(category="image")


def generate_domain_and_ipv4(service: str, team: int, tick: int) -> str:
    faker = _get_deterministic_faker(service, team, tick)
    return json.dumps(
        {
            "domain": faker.domain_name(),
            "ip": faker.ipv4(),
        }
    )


def get_current_tick() -> int:
    return (datetime.now(timezone.utc) - FIRST_TICK_START) // TICK_DURATION + 1
