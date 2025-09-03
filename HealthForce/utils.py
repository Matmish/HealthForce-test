import json
import random
import time
from pathlib import Path

LOG_FILE = Path("out/run.log")


def ensure_outdir():
    Path("out").mkdir(exist_ok=True)


def json_logger(event_code: str, data=None):
    ensure_outdir()
    log = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": event_code,
    }
    if data:
        log["data"] = data
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")


async def paced_wait():
    import asyncio

    delay = random.uniform(0.1, 0.4)
    await asyncio.sleep(delay)


def parse_date(text: str):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
