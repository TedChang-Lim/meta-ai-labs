import asyncio
import json
import os
import time
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from watchfiles import awatch

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).parent
SHARED_DIR = "/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared"

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


# 백그라운드 파일 시스템 감시 태스크
async def watch_agent_activities():
    last_active = {
        "Mimo": 0.0,
        "Hena": 0.0,
        "AG": 0.0,
    }

    # 10초 무활동 시 idle 상태로 자동 복귀 처리
    async def idle_timeout_check():
        global saved_cost
        while True:
            await asyncio.sleep(2)
            now = time.time()
            updated = False
            for agent, last_time in last_active.items():
                if agents_state[agent]["status"] == "busy" and (now - last_time) > 10:
                    agents_state[agent]["status"] = "idle"
                    agents_state[agent]["file"] = "-"
                    updated = True
            if updated:
                await broadcast({"type": "update", "agents": agents_state, "saved_cost": saved_cost})

    asyncio.create_task(idle_timeout_check())

    try:
        async for changes in awatch(SHARED_DIR):
            now = time.time()
            updated = False
            for change_type, filepath in changes:
                filename = os.path.basename(filepath)
                # 시스템 및 git 파일 필터링
                if ".git" in filepath or filename.startswith("."):
                    continue

                target_agent = None
                # 파일 수정 주체 매핑
                if filename == "mimo_chat_log.md" or "to-mimo" in filename:
                    target_agent = "Mimo"
                elif filename == "to-ag.md" or "drafts" in filepath:
                    target_agent = "Hena"
                elif filename == "to-hena.md":
                    target_agent = "AG"

                if target_agent:
                    agents_state[target_agent]["status"] = "busy"
                    agents_state[target_agent]["file"] = filename
                    last_active[target_agent] = now
                    updated = True

            if updated:
                await broadcast({"type": "update", "agents": agents_state, "saved_cost": saved_cost})
    except Exception as e:
        print(f"Error in file watcher: {e}")


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(watch_agent_activities())


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


if __name__ == "__main__":
    uvicorn.run("madcat_server:app", host="0.0.0.0", port=1984, reload=True)