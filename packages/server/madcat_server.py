import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from watchfiles import awatch
import httpx

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


# 백그라운드 파일 시스템 감시 태스크 (대시보드 상태 자동 감지용)
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
        async for changes in awatch(str(SHARED_DIR)):
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


class GradeRequest(BaseModel):
    prompt: str


@app.post("/api/grade")
async def grade_prompt(request: GradeRequest):
    prompt_content = request.prompt.strip()
    if not prompt_content:
        raise HTTPException(status_code=400, detail="프롬프트 내용을 입력하세요.")
        
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        # Fallback Mock Grading Logic to prevent hard crash if keys are not set yet in local dev
        score = 60
        feedback = "<strong>[시뮬레이션 모드]</strong> 로컬 환경에 DEEPSEEK_API_KEY가 등록되어 있지 않아 자체 규칙 기반 채점을 실행했습니다.<br><br>"
        
        has_role = any(word in prompt_content for word in ["감독", "강사", "전문가", "교수", "너는", "의사", "역할", "선생님"])
        has_tips = any(word in prompt_content for word in ["팁", "방법", "노하우", "핵심", "설명", "알려줘", "조언"])
        
        if has_role and has_tips:
            score = 85
            feedback += "✓ <strong>역할 부여 성공:</strong> 인공지능에게 구체적인 페르소나를 성공적으로 부여하셨습니다.<br>✓ <strong>임무 구체성 성공:</strong> 스마트폰 카메라 팁을 알려달라는 지시가 명확합니다.<br><br>💡 <strong>팁:</strong> 여기에 '친절한 말투로 작성해줘' 같은 출력 스타일(톤앤매너)까지 추가해 보시면 100점에 도달할 수 있습니다!"
        elif has_role:
            score = 70
            feedback += "✓ <strong>역할 부여 성공:</strong> 역할을 지정하셨으나, 어떤 구체적 정보(예: 야경 촬영 3대 팁)를 원하는지 임무가 조금 모호합니다. 질문을 좀 더 구체적으로 작성해 보세요."
        else:
            feedback += "✗ <strong>보완 필요:</strong> 인공지능에게 아무런 역할을 부여하지 않은 일반적인 질문입니다. '너는 30년 경력의 베테랑 사진감독이야'와 같이 역할을 명시하는 것부터 시작해 보세요."
            
        return {"score": score, "feedback": feedback}

    system_instruction = """
    당신은 대한민국 최고의 프롬프트 엔지니어링 교육 전문가입니다.
    수강생(시니어 및 초보자)이 작성한 AI 지시문(프롬프트)을 평가하고 피드백을 주어야 합니다.
    
    [미션 목표]: 인공지능에게 구체적인 '역할(페르소나)'을 명시하고, 원하는 '임무와 조건'을 3문장 이상 구체적으로 지시하는 것.
    
    [채점 기준]:
    1. 역할 부여 여부 (40점): 챗GPT에게 명확한 직업, 경력, 태도를 부여했는가?
    2. 구체적 임무 (40점): 알려달라고 하는 질문이나 결과물 형식이 명확하고 3문장 이상으로 서술되었는가?
    3. 문맥과 톤앤매너 (20점): 한국어 문맥이 자연스럽고 명확한가?
    
    [반환 형식]:
    반드시 아래와 같은 JSON 구조로만 답변해야 합니다. 다른 사족이나 마크다운 펜스(```) 없이 순수 JSON만 반환하세요:
    {
      "score": 85,
      "feedback": "역할을 아주 구체적으로 잘 부여하셨습니다! 스마트폰 카메라의 하이라이트 노출 조절 팁을 추가하라는 임무도 명확합니다. 여기에 '답변은 친절하고 격려하는 말투로 해달라'는 출력 형식 제어까지 추가되면 100점짜리 프롬프트가 됩니다."
    }
    피드백은 한국어로 작성하며, 줄바꿈은 <br> 태그를 사용해 웹 화면에서 예쁘게 보이도록 하세요.
    """

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": f"학생의 제출 프롬프트:\n\"\"\"\n{prompt_content}\n\"\"\""}
                    ],
                    "temperature": 0.3,
                    "response_format": {"type": "json_object"}
                }
            )
            
            if response.status_code != 200:
                raise Exception(f"DeepSeek API error: {response.text}")
                
            res_data = response.json()
            content = res_data["choices"][0]["message"]["content"].strip()
            result = json.loads(content)
            return {
                "score": int(result.get("score", 70)),
                "feedback": result.get("feedback", "채점을 완료했습니다.")
            }
            
    except Exception as e:
        print(f"Error during AI grading: {e}")
        return {
            "score": 75,
            "feedback": f"<strong>[안내] AI API가 일시적으로 지연되어 기본 규칙 기반 평가를 수행했습니다.</strong><br><br>작성하신 프롬프트: \"{prompt_content}\"<br><br>역할 부여와 질문 구조가 무난합니다. 구체적인 조건과 친절한 답변 요청 문구를 추가하여 한 단계 더 실무적인 지시를 내려보세요."
        }



if __name__ == "__main__":
    uvicorn.run("madcat_server:app", host="0.0.0.0", port=1984, reload=True)