#!/usr/bin/env python3
"""
cron_briefing.py - 새미새론 AI 데일리 브리핑(모닝샘) 자동 발행 스크립트
- 요약 모델: OpenCode Go 구독 모델 (opencode-go/deepseek-v4.1-flash)
- 20종 히어로 이미지 1:1 매핑
- RSS 피드 수집 -> AI 자체 문장 요약 + So What 3줄 작성 -> today-briefing.json 및 briefing.html 업데이트
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))
TODAY_STR = datetime.now(KST).strftime("%Y.%m.%d")
TODAY_ISO = datetime.now(KST).isoformat()

# 20종 히어로 매핑 테이블 (실물 파일 1:1 검증 완료)
HERO_MAPPING = {
    1:  {"file": "marks/heroes/hero_budget.webp",       "tag": "BUDGET",          "desc": "예산·정책 — 새벽 도시 실루엣"},
    2:  {"file": "marks/heroes/hero_model.webp",        "tag": "MODEL",           "desc": "모델·기술 — 성운 속 회로 강물"},
    3:  {"file": "marks/heroes/hero_classroom.webp",    "tag": "CLASSROOM",       "desc": "교육 — 황혼 교실 빛"},
    4:  {"file": "marks/heroes/hero_senior.webp",       "tag": "SENIOR",          "desc": "시니어 — 빛나는 폰을 든 손"},
    5:  {"file": "marks/heroes/hero_kids.webp",         "tag": "KIDS",            "desc": "어린이 — 장난감 블록 별"},
    6:  {"file": "marks/heroes/hero_flower.webp",       "tag": "FLOWER",          "desc": "힐링 — 어둠 속 봄꽃"},
    7:  {"file": "marks/heroes/hero_ocean.webp",        "tag": "OCEAN",           "desc": "새벽 바다 금빛 물결"},
    8:  {"file": "marks/heroes/hero_space.webp",        "tag": "SPACE",           "desc": "우주 — 지구 일출"},
    9:  {"file": "marks/heroes/hero_city.webp",         "tag": "CITY",            "desc": "도시 야경 창문 불빛"},
    10: {"file": "marks/heroes/hero_library.webp",      "tag": "LIBRARY",         "desc": "도서관 — 책과 등불"},
    11: {"file": "marks/heroes/hero_field.webp",        "tag": "FIELD",           "desc": "들판 일출과 아침 안개"},
    12: {"file": "marks/heroes/hero_hands.webp",        "tag": "HANDS",           "desc": "연대 — 빛을 향한 손들"},
    13: {"file": "marks/heroes/hero_robot.webp",        "tag": "ROBOT",           "desc": "미래 — 작은 로봇과 여명"},
    14: {"file": "marks/heroes/hero_crane.webp",        "tag": "CRANE",           "desc": "희망 — 종이학과 달빛"},
    15: {"file": "marks/heroes/hero_forest.webp",       "tag": "FOREST",          "desc": "숲속 빛기둥과 안개"},
    16: {"file": "marks/heroes/hero_korea_ai.jpg",      "tag": "SOVEREIGN_AI",    "desc": "K-AI·한옥 창호 뉴럴"},
    17: {"file": "marks/heroes/hero_silicon_wafer.jpg", "tag": "SEMICONDUCTOR",   "desc": "반도체·실리콘 웨이퍼"},
    18: {"file": "marks/heroes/hero_quantum_drop.jpg",  "tag": "ORIGIN_DROP",     "desc": "새미새론 물방울 파문"},
    19: {"file": "marks/heroes/hero_supercomputer.jpg", "tag": "INFRASTRUCTURE",  "desc": "데이터센터·슈퍼컴"},
    20: {"file": "marks/heroes/hero_agronomy_ai.jpg",   "tag": "BIO_SMART_AGRI",  "desc": "스마트 바이오 새싹"},
}

RSS_FEEDS = [
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "MIT Tech Review", "url": "https://www.technologyreview.com/feed/"}
]

def fetch_rss_items():
    articles = []
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
    for feed in RSS_FEEDS:
        try:
            req = urllib.request.Request(feed["url"], headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                xml_data = resp.read()
                root = ET.fromstring(xml_data)
                for item in root.findall(".//item")[:4]:
                    title = item.findtext("title", "").strip()
                    link = item.findtext("link", "").strip()
                    desc = item.findtext("description", "").strip()
                    if title:
                        articles.append({
                            "source": feed["name"],
                            "title": title,
                            "link": link,
                            "description": desc[:300]
                        })
        except Exception as e:
            print(f"[RSS Warning] {feed['name']} 실패: {e}")
            continue
    return articles

def call_opencode_go(prompt):
    """OpenCode Go 구독 모델 (deepseek-v4.1-flash) 호출"""
    cmd = [
        "opencode", "run",
        "-m", "opencode-go/deepseek-v4.1-flash",
        "--pure",
        prompt
    ]
    # stdin을 닫고 실행
    proc = subprocess.run(
        cmd,
        input="",
        text=True,
        capture_output=True,
        timeout=60
    )
    raw_output = proc.stdout
    # opencode 헤더 제거 후 JSON 부분만 추출
    lines = raw_output.split("\n")
    json_lines = []
    started = False
    for line in lines:
        if "{" in line and not started:
            started = True
        if started:
            json_lines.append(line)
    
    text = "\n".join(json_lines).strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

def generate_briefing(articles):
    day_num = datetime.now(KST).day
    default_hero_id = ((day_num - 1) % 20) + 1

    prompt = f"""
당신은 '새미새론 AI 교육원'의 모닝 브리핑 수석 에디터입니다.
저작권 원칙: 뉴스 원문을 그대로 복사하지 말고, 100% 자체 문장으로 재작성하십시오.
문체 원칙: 사람이 아침에 읽어도 어색하지 않은 평범하고 따뜻한 문체. 윤리적으로 문제될 표현, 과도한 성적 묘사, 선정적 표현은 절대 금지. 정보는 정확히 전달하되, 가끔 가벼운 위트 한 스푼을 곁들이십시오.

오늘 수집된 글로벌 AI 뉴스 목록:
{json.dumps(articles[:5], ensure_ascii=False, indent=2)}

오직 유효한 JSON 포맷 하나만 출력하십시오. 인사말이나 마크다운 백틱도 출력하지 마십시오.

{{
  "hero_id": {default_hero_id},
  "ticker": {{
    "badge": "오늘의 AI 핵심",
    "headline": "한국어 1줄 핵심 헤드라인 (35자 내외)",
    "link": "briefing.html"
  }},
  "focus_news": {{
    "tag": "MODEL & REASONING",
    "title": "가장 중요한 메인 기사의 품격 있는 한국어 제목",
    "summary": "핵심 내용에 대한 3~4문장의 명쾌하고 쉬운 자체 분석 요약",
    "so_what": "새미새론 관점: 1) 업무 적용점, 2) 교육적 가치, 3) 향후 전망을 담은 3개 문장",
    "source_name": "언론사 출처명",
    "source_url": "원문 링크"
  }},
  "daily_three": [
    {{
      "id": 1,
      "category": "HARDWARE",
      "title": "두 번째 중요 기사 한국어 제목",
      "one_line": "실무자가 알아야 할 핵심 포인트 1줄 요약"
    }},
    {{
      "id": 2,
      "category": "POLICY",
      "title": "세 번째 중요 기사 한국어 제목",
      "one_line": "실무자가 알아야 할 핵심 포인트 1줄 요약"
    }},
    {{
      "id": 3,
      "category": "EDUCATION",
      "title": "네 번째 중요 기사 한국어 제목",
      "one_line": "실무자가 알아야 할 핵심 포인트 1줄 요약"
    }}
  ]
}}
"""
    return call_opencode_go(prompt)

def main():
    print(f"[{TODAY_STR}] OpenCode Go (DeepSeek v4.1 Flash) 기반 모닝샘 크론 작업 시작...")
    articles = fetch_rss_items()
    if not articles:
        articles = [
            {"source": "TechCrunch AI", "title": "New Frontier AI Models Focus on Autonomous Reasoning and Planning", "link": "https://techcrunch.com", "description": "Frontier AI lab releases new agentic reasoning architecture."},
            {"source": "MIT Tech Review", "title": "Next-Gen AI Semiconductor Breakthrough Reduces Data Center Power", "link": "https://technologyreview.com", "description": "Hardware breakthrough lowers inference compute cost."}
        ]

    fallback_source = articles[0]["source"] if articles else "TechCrunch / Global AI Hub"
    fallback_url = articles[0]["link"] if articles else "https://techcrunch.com/category/artificial-intelligence/"

    try:
        data = generate_briefing(articles)
        print("OpenCode Go 요약 생성 성공!")
    except Exception as e:
        print(f"OpenCode Go 호출 예외: {e}. 백업 규격 데이터를 적용합니다.")
        day_num = datetime.now(KST).day
        hid = ((day_num - 1) % 20) + 1
        data = {
            "hero_id": hid,
            "ticker": {
                "badge": "오늘의 AI 핵심",
                "headline": "글로벌 AI 연구소들의 자율 에이전트 및 하드웨어 혁신 가속화",
                "link": "briefing.html"
            },
            "focus_news": {
                "tag": "FRONTIER AI",
                "title": "자율 추론과 에이전트 오케스트레이션이 이끄는 2026 AI 패러다임 전환",
                "summary": "단순 프롬프트 입출력을 넘어 복합 태스크를 스스로 계획하고 실행하는 에이전트 시스템이 산업 전반의 표준으로 자리잡고 있습니다.",
                "so_what": "새미새론 관점: 업무 자동화의 수준이 개인 도구를 넘어 조직 단위 워크플로우로 확장되고 있으므로, 에이전트 협업 역량이 핵심 경쟁력이 됩니다.",
                "source_name": fallback_source,
                "source_url": fallback_url
            },
            "daily_three": [
                {"id": 1, "category": "COMPUTE", "title": "차세대 반도체 공정, LLM 전력 소모 대폭 절감", "one_line": "추론 인프라 비용 절감으로 엔터프라이즈 도입 속도 가속화 전망."},
                {"id": 2, "category": "EDUCATION", "title": "글로벌 AI 교육 혁신, 실무 프로젝트 중심 개편", "one_line": "이론 중심에서 실전 파이프라인 구축 중심의 커리큘럼 전환 확산."},
                {"id": 3, "category": "OPEN SOURCE", "title": "고성능 오픈 가중치 모델 공개로 생태계 확장", "one_line": "로컬 프라이빗 AI 구축을 원하는 기업들에게 강력한 대안 제공."}
            ]
        }

    # 히어로 매핑 보정
    hid = data.get("hero_id", 1)
    if hid not in HERO_MAPPING:
        hid = 1
    data["hero_id"] = hid
    data["hero_image"] = HERO_MAPPING[hid]["file"]
    data["hero_tag"] = HERO_MAPPING[hid]["tag"]
    data["date"] = TODAY_STR
    data["updated_at"] = TODAY_ISO
    # 호수: 9/10 시안=제1호, 9/15 정식 첫발행=제2호부터 하루 1씩 증가
    try:
        from datetime import date as _date
        _second = _date(2026, 9, 15)
        _today = datetime.now(KST).date()
        data["issue_no"] = 1 if _today < _second else (_today - _second).days + 2
    except Exception:
        data["issue_no"] = 1

    # 파일 저장 (today-briefing.json)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "today-briefing.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"성공: {json_path} 저장 완료 (Hero #{hid}: {data['hero_image']})")

if __name__ == "__main__":
    main()
