import httpx
from datetime import datetime, timezone
import time
import argparse
import random

CAM_IDS = ["CAM-01", "CAM-02", "CAM-03", "CAM-04", "CAM-05"]
EVENT_TYPES = ["intrusion", "loitering", "departure", "entry", "stationary/abandoned"]


def generate_event() -> dict[str, object]:
    return {
        "camera_id": random.choice(CAM_IDS),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": random.choice(EVENT_TYPES),
        "confidence": round(random.uniform(0.5, 1.0), 2),
    }


def run(rate: float, url: str) -> None:
    print(
        f"Sending events to {url} at {rate} units per second (press Ctrl + C to stop)"
    )
    while True:
        event = generate_event()
        try:
            response = httpx.post(f"{url}/events", json=event, timeout=5.0)
            print(
                f"Sent: {event['event_type']} from {event['camera_id']} — status {response.status_code}"
            )
        except httpx.ConnectError:
            print("Cannot connect, check if the server is running.")
        time.sleep(1 / rate)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sentinel Event Simulator")
    parser.add_argument("--rate", type=float, default=1.0, help="Events per second")
    parser.add_argument(
        "--url", type=str, default="http://127.0.0.1:8000", help="API base URL"
    )
    args = parser.parse_args()
    run(args.rate, args.url)
