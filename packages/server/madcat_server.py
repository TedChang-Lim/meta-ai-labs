import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
SHARED_DIR = Path.home() / "초보프로젝트" / "hermes-ag-shared"
MESSAGES_DIR = SHARED_DIR / "messages"
ARCHIVE_DIR = SHARED_DIR / "archive"

MESSAGES_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

agents_state = {
    "Hena": {"status": "idle", "file": "-", "cost": 0.0},
    "AG": {"status": "idle", "file": "-", "cost": 0.0},
    "Mimo": {"status": "idle", "file": "-", "cost": 0.0},
    "Q": {"status": "idle", "file": "-", "cost": 0.0},
    "Jan": {"status": "idle", "file": "-", "cost": 0.0},
}

saved_cost = 0.0
app.client_queues = []


class AgentUpdate(BaseModel):
    agent: str
    status: str
    file: Optional[str] = "-"
    cost: Optional[float] = 0.0
    saved: Optional[float] = 0.0


class MessageAdd(BaseModel):
    agent: str
    content: str


async def event_generator(request: Request):
    client_queue = asyncio.Queue()
    app.client_queues.append(client_queue)
    try:
        yield f"data: {json.dumps({'type': 'init', 'agents': agents_state, 'saved_cost': saved_cost})}\n\n"
        while True:
            if await request.is_disconnected():
                break
            try:
                msg = await asyncio.wait_for(client_queue.get(), timeout=1.0)
                yield f"data: {json.dumps(msg)}\n\n"
            except asyncio.TimeoutError:
                yield f": heartbeat\n\n"
    finally:
        app.client_queues.remove(client_queue)


async def broadcast(message: dict):
    for queue in app.client_queues:
        await queue.put(message)


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = BASE_DIR / "dashboard.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/state")
async def get_state():
    return {"agents": agents_state, "saved_cost": saved_cost}


@app.post("/update")
async def update_state(data: AgentUpdate):
    global saved_cost
    if data.agent in agents_state:
        agents_state[data.agent]["status"] = data.status
        agents_state[data.agent]["file"] = data.file
        agents_state[data.agent]["cost"] = data.cost
    if data.saved > 0:
        saved_cost += data.saved
    await broadcast({"type": "update", "agents": agents_state, "saved_cost": saved_cost})
    return {"status": "success"}


@app.get("/stream")
async def stream(request: Request):
    return StreamingResponse(event_generator(request), media_type="text/event-stream")


@app.post("/stop")
async def stop_server():
    await broadcast({"type": "stop"})
    os._exit(0)


@app.get("/messages")
async def list_messages():
    messages = []
    if MESSAGES_DIR.exists():
        for file in MESSAGES_DIR.glob("*.md"):
            stat = file.stat()
            messages.append({
                "filename": file.name,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
    return {"messages": messages, "count": len(messages)}


@app.get("/messages/{filename}")
async def read_message(filename: str):
    file_path = MESSAGES_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Message not found")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return {"filename": filename, "content": content}


@app.post("/messages/{filename}")
async def add_message(filename: str, data: MessageAdd):
    file_path = MESSAGES_DIR / filename
    timestamp = datetime.now().isoformat()
    message_line = json.dumps({
        "timestamp": timestamp,
        "agent": data.agent,
        "content": data.content,
    }, ensure_ascii=False)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(message_line + "\n")
    await broadcast({
        "type": "message",
        "filename": filename,
        "agent": data.agent,
        "timestamp": timestamp,
    })
    return {"status": "success", "timestamp": timestamp}


@app.post("/messages/{filename}/read")
async def mark_as_read(filename: str):
    file_path = MESSAGES_DIR / filename
    archive_path = ARCHIVE_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Message not found")
    file_path.rename(archive_path)
    await broadcast({"type": "archived", "filename": filename})
    return {"status": "success", "archived_to": str(archive_path)}


if __name__ == "__main__":
    uvicorn.run("madcat_server:app", host="0.0.0.0", port=1984, reload=True)