# Notes on Async IO in Python

## What is Async IO?

Async IO is a way to enable a single thread in a computer to carry out multiple tasks that have waiting times concurrently (NOT parallel) without idle standby during said waiting periods. The main terminology used alongside the `asyncio` library in Python are `await` and `async def`. When a "coroutine" (one of these tasks with waiting time) hits an await, it pauses and gives control back to the event loop to allow other coroutines to run in the meantime. Once the awaited operation is done, the event loop hands control back to the paused coroutine from where it left off. The key thing is that nothing actually runs in parallel: there's still only one thread doing work at any given moment, but because waiting doesn't block, a single thread can juggle hundreds of non-computationally heavy in-progress tasks efficiently.

## Async IO vs Threading

Async is the right tool when a task spends most of its time waiting on I/O to process (i.e, network requests, database queries, file reads). While one coroutine is waiting, the event loop can run hundreds of others on a single thread. This is extremely efficient because waiting doesn't cost CPU time, and rather than causing waiting time to block other coroutines from being executed, Async IO can help to concurrently move from one coroutine to another while awaiting for operations to complete in the meantime.

Threads (or multiprocessing) is the right tool for CPU-bound work, that is, actual computationally heavy stuff that keeps the processor busy, like image processing or encryption. Async doesn't help here because the event loop has nowhere to switch to (the CPU is occupied the whole time, no idle waiting time that could be efficiently used).

## Examples of the use cases of Async IO vs Threading

**Async IO:** The WebSocket broadcaster in main.py is a situation where Async IO was required. When the server has 50 connected clients and a new event arrives, it needs to send that event to all 50 of them. Each `send_text()` call is a network
operation that takes a small but non-zero amount of time. With async, the server can have all 50 sends "in flight" at once rather than sending to client 1, waiting for it to finish, then client 2, and so on. This is why the broadcast loop uses `await connection.send_text(message)` inside an async function.

**Threading:** If this service ever needed to run real anomaly detection on camera frames (actual image analysis or computer vision processing rather than the simulated events we're using), that would be CPU-bound work. Running it with async wouldn't help as the CPU would still be fully occupied processing-power wise, and there'd be nothing for the event loop to switch to. That kind of work would need a thread pool or a separate worker process so it doesn't block the WebSocket broadcaster from doing its job.


