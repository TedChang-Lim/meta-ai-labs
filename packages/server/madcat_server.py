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
from collections import defaultdict
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
    course: str = "basics"
    mission: int = 0


# Simple memory-based rate limiter (IP -> timestamps)
RATE_LIMIT_STRIKES = defaultdict(list)

def check_rate_limit(ip: str, limit: int = 5, window: int = 60) -> bool:
    current_time = time.time()
    # Filter out timestamps older than the window
    RATE_LIMIT_STRIKES[ip] = [t for t in RATE_LIMIT_STRIKES[ip] if current_time - t < window]
    
    if len(RATE_LIMIT_STRIKES[ip]) >= limit:
        return False
        
    RATE_LIMIT_STRIKES[ip].append(current_time)
    return True


def local_grading(course: str, mission: int, prompt: str) -> dict:
    prompt_content = prompt.strip()
    passed = 0
    feedback_items = []
    
    if course == "basics":
        if mission == 0:  # Mission 01: 3요소 마스터
            has_role = any(word in prompt_content for word in ["로서", "전문가", "마케터", "감독", "강사", "교수", "선생님", "의사", "바리스타", "작가", "컨설턴트", "너는", "당신은"])
            has_task = any(word in prompt_content for word in ["작성", "해줘", "알려줘", "만들어줘", "설명해줘", "가르쳐줘", "정리해줘"])
            has_context = any(word in prompt_content for word in ["치킨", "프로모션", "주말", "세일", "할인", "이벤트", "가게"])
            
            if has_role:
                passed += 1
                feedback_items.append("✓ <strong>역할 부여 성공:</strong> 인공지능에게 구체적인 페르소나를 성공적으로 부여하셨습니다.")
            else:
                feedback_items.append("✗ <strong>역할 누락:</strong> 인공지능에게 아무런 역할을 지정하지 않았습니다. <em>예: '마케팅 전문가로서'</em>와 같이 역할을 지정해 보세요.")
                
            if has_task:
                passed += 1
                feedback_items.append("✓ <strong>구체적 요청 성공:</strong> 공지글 작성을 요청하는 명확한 요청 동사가 포함되었습니다.")
            else:
                feedback_items.append("✗ <strong>요청 누락:</strong> 인공지능이 무엇을 해야 하는지 명령어가 모호합니다. <em>예: 'SNS 공지글을 작성해줘'</em>와 같이 지시해 보세요.")
                
            if has_context:
                passed += 1
                feedback_items.append("✓ <strong>맥락 포함 성공:</strong> 치킨집 프로모션 배경 정보를 적절히 포함하셨습니다.")
            else:
                feedback_items.append("✗ <strong>맥락 부족:</strong> 치킨집이나 주말 할인 등의 핵심 배경 정보가 부족합니다. 지문에 제시된 상황을 덧붙여 주세요.")

        elif mission == 1:  # Mission 02: 문서 요약
            has_length = any(word in prompt_content for word in ["문장", "줄", "글자", "간단히", "요약"])
            has_target = any(word in prompt_content for word in ["초등학생", "쉽게", "어린이", "초보자", "이해"])
            has_format = any(word in prompt_content for word in ["키워드", "따로", "별도", "추출", "뽑아"])
            
            if has_length:
                passed += 1
                feedback_items.append("✓ <strong>분량 지정 성공:</strong> 3문장 이내 요약 등의 분량 조건이 명시되었습니다.")
            else:
                feedback_items.append("✗ <strong>분량 누락:</strong> 요약 결과물의 분량 제한 조건이 빠져 있습니다. <em>예: '3문장 이내로 요약해줘'</em>")
                
            if has_target:
                passed += 1
                feedback_items.append("✓ <strong>난이도/대상 지정 성공:</strong> 초등학생 기준 등의 눈높이 조건이 포함되었습니다.")
            else:
                feedback_items.append("✗ <strong>대상 누락:</strong> 이해 대상(초등학생 등)이나 쉽게 설명해 달라는 조건이 누락되었습니다.")
                
            if has_format:
                passed += 1
                feedback_items.append("✓ <strong>출력 형식 지정 성공:</strong> 키워드 3개 별도 추출 조건이 반영되었습니다.")
            else:
                feedback_items.append("✗ <strong>형식 누락:</strong> '핵심 키워드 3개 추출'과 같은 출력 형식을 명시해 보세요.")

        else:  # Mission 03: 이미지 프롬프트
            has_subject = any(word in prompt_content for word in ["여성", "사람", "공원", "벤치", "책", "가을"])
            has_style = any(word in prompt_content for word in ["수채화", "유화", "사진", "일러스트", "스타일", "화풍"])
            has_mood = any(word in prompt_content for word in ["따뜻", "아늑", "평화", "쓸쓸", "가을", "분위기"])
            has_composition = any(word in prompt_content for word in ["클로즈업", "배경", "구도", "앵글", "배치", "줌"])
            
            if has_subject: passed += 1
            if has_style: passed += 1
            if has_mood: passed += 1
            if has_composition: passed += 1
            
            feedback_items.append(f"✓ <strong>조건 매칭:</strong> 이미지 4대 요소 중 {passed}개 요소를 매핑하셨습니다.")
            if not has_subject: feedback_items.append("✗ <strong>주제 누락:</strong> 그릴 대상을 묘사해 주세요.")
            if not has_style: feedback_items.append("✗ <strong>스타일 누락:</strong> 화풍(예: 수채화 스타일)을 지정해 주세요.")
            if not has_mood: feedback_items.append("✗ <strong>분위기 누락:</strong> 느낌(예: 따뜻한 분위기)을 추가해 주세요.")
            if not has_composition: feedback_items.append("✗ <strong>구도 누락:</strong> 카메라 앵글(예: 클로즈업)을 덧붙여 보세요.")

    elif course == "marketing":
        if mission == 0:  # Mission 01: 상품 카피라이팅
            has_role = any(word in prompt_content for word in ["카피라이터", "마케터", "전문가", "작가", "너는"])
            has_product = any(word in prompt_content for word in ["비누", "라벤더", "꿀", "올리브"])
            has_target = any(word in prompt_content for word in ["여성", "피부", "건성", "민감성", "타겟", "고객", "감성"])
            has_price = any(word in prompt_content for word in ["12,000", "12000", "만원"])
            
            if has_role: passed += 1
            if has_product: passed += 1
            if has_target: passed += 1
            if has_price: passed += 1
            
            feedback_items.append(f"✓ <strong>조건 매칭:</strong> 마케팅 필수 조건 중 {passed}/4개를 포함하셨습니다.")
            if not has_role: feedback_items.append("✗ <strong>역할 누락:</strong> 카피라이터/마케터 역할을 지정하세요.")
            if not has_product: feedback_items.append("✗ <strong>제품 정보 누락:</strong> 제품 성분 정보가 필요합니다.")
            if not has_target: feedback_items.append("✗ <strong>타겟/톤 누락:</strong> 고객군이나 감성 톤을 추가해 보세요.")
            if not has_price: feedback_items.append("✗ <strong>가격 누락:</strong> 가격(12,000원)을 반드시 지시문에 넣어야 합니다.")
            
        else:  # Mission 02: SNS 홍보 문구
            has_sns = any(word in prompt_content for word in ["인스타", "SNS", "게시물", "피드", "홍보"])
            has_season = any(word in prompt_content for word in ["가을", "겨울", "따뜻", "아늑", "계절"])
            has_tag = "#" in prompt_content
            has_visit = any(word in prompt_content for word in ["방문", "오세요", "놀러", "맛보", "추천", "카페"])
            
            if has_sns: passed += 1
            if has_season: passed += 1
            if has_tag: passed += 1
            if has_visit: passed += 1
            
            feedback_items.append(f"✓ <strong>조건 매칭:</strong> SNS 기획 필수 조건 중 {passed}/4개를 포함하셨습니다.")
            if not has_sns: feedback_items.append("✗ <strong>매체 누락:</strong> 인스타그램 게시물 형식 임을 알려주세요.")
            if not has_season: feedback_items.append("✗ <strong>계절감 누락:</strong> 가을/겨울 신메뉴임을 드러내 주세요.")
            if not has_tag: feedback_items.append("✗ <strong>해시태그 누락:</strong> '#' 기호가 포함된 태그 지시가 없습니다.")
            if not has_visit: feedback_items.append("✗ <strong>행동 유도 누락:</strong> 방문 유도 멘트 작성을 요청하세요.")
            
    else:
        # Fallback placeholder for other courses
        passed = 3
        feedback_items.append("✓ 임시 로컬 채점을 성공적으로 완료했습니다.")

    # Calculate score based on passed conditions
    total_checks = 4 if (course == "basics" and mission == 2) or (course == "marketing") else 3
    success_ratio = passed / total_checks
    
    if success_ratio >= 0.75:
        score = 80
        status_feedback = "<strong>[일반 체험 모드 - 합격]</strong> 체험 미션 조건을 훌륭하게 통과하셨습니다! 🥳<br><br>"
    elif success_ratio >= 0.5:
        score = 50
        status_feedback = "<strong>[일반 체험 모드 - 보완 필요]</strong> 약간의 조건이 누락되었습니다. 아래 팁을 보고 보완해 보세요!<br><br>"
    else:
        score = 20
        status_feedback = "<strong>[일반 체험 모드 - 재도전]</strong> 프롬프트 요소를 더 채워서 다시 작성해 보세요.<br><br>"
        
    return {"score": score, "feedback": status_feedback + "<br>".join(feedback_items), "mode": "sandbox"}


@app.post("/api/grade")
async def grade_prompt(request: GradeRequest, fastapi_request: Request):
    prompt_content = request.prompt.strip()
    if not prompt_content:
        raise HTTPException(status_code=400, detail="프롬프트 내용을 입력하세요.")
        
    # Rate Limit Check (5 requests per minute)
    client_ip = fastapi_request.client.host if fastapi_request.client else "127.0.0.1"
    if not check_rate_limit(client_ip, limit=5, window=60):
        raise HTTPException(status_code=429, detail="요청이 너무 빈번합니다. 1분 후에 다시 시도해 주세요.")
        
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
        return local_grading(request.course, request.mission, prompt_content)

    # 3. 정식 수강생 모드 -> DeepSeek API 호출
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        res = local_grading(request.course, request.mission, prompt_content)
        res["feedback"] = "<strong>[정식 수강생 모드 - API 설정 대기]</strong> 인증 코드가 확인되었으나 서버의 DEEPSEEK_API_KEY가 활성화되지 않아 로컬 채점을 임시 작동했습니다.<br><br>" + res["feedback"]
        res["mode"] = "exam"
        return res

    # Dynamic System Instruction mapping
    system_instructions = {
        ("basics", 0): """
        [역할]: 대한민국 최고의 프롬프트 엔지니어링 전문가.
        [미션]: 3대 요소(역할, 맥락, 요청)를 포함해 '주말 프로모션 치킨집 공지글' 프롬프트 채점.
        [채점 기준]: 역할 부여(40점), 구체적 요청(40점), 맥락/배경 설명(20점).
        """,
        ("basics", 1): """
        [역할]: 요약 및 정보 가공 전문가.
        [미션]: 뉴스 기사를 '3문장 이내', '초등학생 눈높이', '핵심 키워드 3개 별도 추출' 하도록 지시하는 프롬프트 채점.
        [채점 기준]: 분량 지정(30점), 난이도 조절(30점), 출력 형식 제어(40점).
        """,
        ("basics", 2): """
        [역할]: AI 이미지 생성 프롬프트 전문가.
        [미션]: 가을 단풍 공원 책 읽는 여성을 그리기 위한 4대 요소(주제, 스타일, 분위기, 구도)를 포함한 프롬프트 채점.
        [채점 기준]: 주제(25점), 스타일(25점), 분위기(25점), 구도(25점).
        """,
        ("marketing", 0): """
        [역할]: 소상공인 마케팅 카피라이팅 전문가.
        [미션]: '라벤더 꿀 비누' 신제품 온라인 스토어 소개글 프롬프트 채점.
        [채점 기준]: 전문가 역할(20점), 제품 성분 정보(30점), 타겟/감성 톤 지정(30점), 가격 명시(20점).
        """,
        ("marketing", 1): """
        [역할]: 소상공인 SNS 마케팅 전문가.
        [미션]: 카페 가을 신메뉴 '고구마 라떼' 인스타그램 홍보 피드 프롬프트 채점.
        [채점 기준]: 매체 명시(25점), 계절감 표현(25점), 해시태그 3개 조건(25점), 방문 유도 멘트(25점).
        """
    }
    
    key = (request.course, request.mission)
    selected_instruction = system_instructions.get(key, """
    당신은 프롬프트 채점 전문가입니다. 학생의 프롬프트를 성의 있게 평가하고 피드백을 주세요.
    """)
    
    system_instruction = f"""
    {selected_instruction}
    
    [반환 형식]:
    반드시 아래와 같은 JSON 구조로만 답변해야 합니다. 다른 사족이나 마크다운 펜스(```) 없이 순수 JSON만 반환하세요:
    {{
      "score": 85,
      "feedback": "피드백 내용을 한국어로 구체적이고 부드러운 어조로 적어주세요. 줄바꿈은 <br> 태그를 사용하세요."
    }}
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
        res = local_grading(request.course, request.mission, prompt_content)
        res["feedback"] = "<strong>[정식 수강생 모드 - API 오류 임시 우회]</strong> AI 응답이 지연되어 로컬 규칙 기반 평가를 임시 수행했습니다.<br><br>" + res["feedback"]
        res["mode"] = "exam"
        return res



if __name__ == "__main__":
    uvicorn.run("madcat_server:app", host="0.0.0.0", port=1984, reload=True)