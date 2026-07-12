# Sentinel Prime AI - Asynchronity + WebSockets

Hello! This is a REST + WebSocket service I built, modeled after Sentinel Prime's anomaly event detection system. It takes in random synthetically generated camera events over a REST and broadcasts them live in real time to a list of "n" connected Websocket clients (here n is random, as per the user's choice on how many endpoints to connect) with a simple HTML page (established with vanilla Javascript for Websocket handling) to observe the live feed.

## How to run it

(Do note that you must have Git and Python 3.11+ downloaded on your system before you can run these commands)

1. Clone the repo using git clone

```bash
git https://github.com/ShaunTheSheep25/sentinel-events.git
cd sentinel-events
```

Note: If you're using pyenv, set up the environment first:
```bash
pyenv virtualenv 3.11 sentinel-events
pyenv local sentinel-events
```

2. Install dependencies with pip (taken care of in the pyproject.toml file)

```bash
pip install -e ".[dev]"
```

3. Run the server using uvicorn

```bash
uvicorn sentinel_events.main:app --reload
```

4. In a second terminal, run the simulator script to generate synthetic events.

```bash
python scripts/simulate.py --rate 1
```

5. Open `static/live.html` directly in your browser to see the live feed update in real time.

6. (Optional) Visit the link `http://127.0.0.1:8000/docs` on your browser, for the interactive documentation available on Swagger UI to manually test each event endpoint of the RestAPI. 

## How to test it

To test the RestAPI, you can run pytest with or without coverage, depending on the level of detail you'd want in the final report.

```bash
pytest tests/                   # simple testing, no coverage
pytest --cov=src tests/         # miss-rate coverage report of testing script
```

## Limitations + How I'd fix them

There are a few limitations I've come to observe while working on this project, and I'd like to fix them as shown -

- The event store is in-memory only (all events are lost on server restart) and can only take a maximum of 500 events, so I'd take measures to add said event data to a PostgreSQL relational database (using SQLAlchemy to translate the Pydantic schema into a working model)
- There's no authentication on the Websocket endpoint and anyone could connect to the Websocket connection manager, so I'd look into implementing that using `python-jose` (JWT authentication)
- The HTML demo page is intentionally minimal, so I'd like to make it more user-friendly and approachable
- Add filtering on the live feed (by camera, by event type, confidence and threshold) + add a heartbeat/ping-pong mechanism to detect dead connections faster, so that we can shift priorities to the more active connections and ensure efficient transmission



