from fastapi import WebSocket, WebSocketDisconnect, HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sentinel_events.models import Event
from sentinel_events import store

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        if ws in self.active_connections:
            self.active_connections.remove(ws)

    async def broadcast(self, message: str) -> None:
        for con in self.active_connections.copy():
            try:
                await con.send_text(message)
            except Exception:
                self.disconnect(con)


cm = ConnectionManager()


@app.post("/events")
async def post_events(event: Event) -> dict[str, object]:
    store.add(event)
    await cm.broadcast(event.model_dump_json())
    event_id = len(store.get_all()) - 1
    return {"id": event_id, "event": event.model_dump()}


@app.get("/events/{event_id}")
async def get_events(event_id: int) -> Event:
    event = store.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")
    return event


@app.get("/events")
async def list_events(limit: int = 10) -> list[Event]:
    all_events = store.get_all()
    return all_events[-limit:]


@app.websocket("/ws/events")
async def ws_endpoint(websocket: WebSocket) -> None:
    await cm.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        cm.disconnect(websocket)
