from collections import deque
from sentinel_events.models import Event

d: deque[Event] = deque(maxlen=100)


def add(event: Event) -> None:
    d.append(event)


def get_all() -> list[Event]:
    return list(d)


def get_by_id(event_id: int) -> Event | None:
    try:
        return list(d)[event_id]
    except IndexError:
        return None
