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

def load_env_file():
    env_path = BASE_DIR.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

load_env_file()

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
        messages.sort(key=lambda x: x["modified"], reverse=True)
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
    passcode: str = ""


def local_grading(prompt: str) -> dict:
    prompt_content = prompt.strip()
    passed = 0
    feedback_items = []
    
    # 🎭 역할 부여 검사 (Role check)
    has_role = any(word in prompt_content for word in ["로서", "처럼", "전문가", "감독", "강사", "교수", "선생님", "의사", "바리스타", "작가", "컨설턴트", "너는", "당신은"])
    if has_role:
        passed += 1
        feedback_items.append("✓ <strong>역할 부여 성공:</strong> 인공지능에게 구체적인 페르소나를 성공적으로 부여하셨습니다.")
    else:
        feedback_items.append("✗ <strong>역할 누락:</strong> 인공지능에게 아무런 역할을 지정하지 않았습니다. <em>예: '너는 30년 경력의 베테랑 사진감독이야'</em>와 같이 역할을 지정해 보세요.")
        
    # 🎯 구체적 요청 검사 (Task check)
    has_task = any(word in prompt_content for word in ["해줘", "알려줘", "작성해줘", "설명해줘", "가르쳐줘", "정리해줘", "추천해줘", "제안해줘"])
    if has_task:
        passed += 1
        feedback_items.append("✓ <strong>구체적 지시 성공:</strong> AI가 무엇을 해야 하는지 명확한 명령어가 포함되었습니다.")
    else:
        feedback_items.append("✗ <strong>임무 누락:</strong> 인공지능이 수행할 명령어가 모호합니다. <em>예: '야경 사진을 촬영하기 위한 3대 핵심 팁을 친절하게 설명해줘'</em>와 같이 구체적으로 지시해 보세요.")
        
    # 📏 최소 길이 검사 (Length check)
    has_length = len(prompt_content) >= 20
    if has_length:
        passed += 1
        feedback_items.append("✓ <strong>최소 분량 충족:</strong> AI가 맥락을 파악할 수 있는 최소 20자 이상의 내용이 기술되었습니다.")
    else:
        feedback_items.append("✗ <strong>분량 부족:</strong> 지시문이 너무 짧습니다. (현재 20자 미만) AI가 풍부한 답을 낼 수 있도록 상황이나 조건을 20자 이상으로 덧붙여 보세요.")

    if passed == 3:
        score = 80
        status_feedback = "<strong>[일반 체험 모드 - 합격]</strong> 일반 체험 미션의 3대 핵심 규칙을 모두 통과하셨습니다! 🥳<br><br>"
    elif passed == 2:
        score = 50
        status_feedback = "<strong>[일반 체험 모드 - 보완 필요]</strong> 한 가지 조건이 더 필요합니다. 아래의 조언을 참고하여 지시문을 다시 수정해 보세요!<br><br>"
    else:
        score = 20
        status_feedback = "<strong>[일반 체험 모드 - 재도전]</strong> 프롬프트의 기본 요소를 더 작성해 주세요. 아래 예시를 참고하여 다시 작성해 보실 수 있습니다.<br><br>"
        
    final_feedback = status_feedback + "<br>".join(feedback_items)
    return {"score": score, "feedback": final_feedback, "mode": "sandbox"}


@app.post("/api/grade")
async def grade_prompt(request: GradeRequest):
    prompt_content = request.prompt.strip()
    if not prompt_content:
        raise HTTPException(status_code=400, detail="프롬프트 내용을 입력하세요.")
        
    # 1. 인증코드 검증
    configured_passcode = os.environ.get("KACEC_PASSCODE", "kacec2026").strip()
    is_valid_passcode = False
    
    if configured_passcode.lower() == "auto_date":
        today_str = datetime.now().strftime("%m%d")
        today_code = f"kacec{today_str}"
        is_valid_passcode = (request.passcode.strip() == today_code)
    else:
        is_valid_passcode = (request.passcode.strip() == configured_passcode)

    # 2. 체험 모드(인증코드가 없거나 틀렸을 때) -> 로컬 채점 실행
    if not is_valid_passcode:
        return local_grading(prompt_content)

    # 3. 정식 수강생 모드 -> DeepSeek API 호출
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        # 인증코드는 맞지만 API Key 세팅 대기 상태일 때 예외 처리
        res = local_grading(prompt_content)
        res["feedback"] = "<strong>[정식 수강생 모드 - API 설정 대기]</strong> 인증 코드가 확인되었으나 서버의 DEEPSEEK_API_KEY가 활성화되지 않아 로컬 채점을 임시 작동했습니다.<br><br>" + res["feedback"]
        res["mode"] = "exam"
        return res

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
                "feedback": result.get("feedback", "채점을 완료했습니다."),
                "mode": "exam"
            }
            
    except Exception as e:
        print(f"Error during AI grading: {e}")
        res = local_grading(prompt_content)
        res["feedback"] = "<strong>[정식 수강생 모드 - API 오류 임시 우회]</strong> AI 응답이 지연되어 로컬 규칙 기반 평가를 임시 수행했습니다.<br><br>" + res["feedback"]
        res["mode"] = "exam"
        return res



if __name__ == "__main__":
    uvicorn.run("madcat_server:app", host="0.0.0.0", port=1984, reload=True)