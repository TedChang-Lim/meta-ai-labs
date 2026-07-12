---
type: concept
created: 2026-06-28
updated: 2026-06-28
sources: [raw/to-ag.md]
aliases: [insane-search, insane-extract]
---

# Insane Search — 에이전트 무적 웹 크롤링 도입기

## 개요
2026년 6월 28일, 에이전트 팀이 웹 방화벽(WAF, Cloudflare 등) 및 봇 탐지로 인해 발생하는 크롤링 실패 문제를 해결하기 위해 한국인 개발자 지피타쿠(GPTaku/FIVETAKU)의 오픈소스 도구 **Insane Search**를 CLI 형태로 공동 장착한 에피소드를 기록한다.

## 배경
- 에이전트들이 웹 검색 본문 수집(`read_url_content`) 시 네이버, 쿠팡, 레딧, 유튜브 등에서 봇 감지(403 Forbidden, WAF 챌린지)로 인해 본문 요약 작업이 빈번히 중단됨.
- 비싼 유료 프록시 서비스 대신 로컬 자원만 사용하여 **추가 비용 0원($0)**으로 해결할 수 있는 가성비 솔루션 필요.

## 해결책: Insane Search 우회 원리 (Phase 0~3 적응형)
상대의 차단 강도에 따라 적절한 무기를 선택하여 실행된다.
1. **Phase 0 (공식 API/전용 파서)**: 유튜브(yt-dlp), HN API 등
2. **Phase 1 (TLS Impersonation)**: `curl_cffi`를 통해 Safari/Chrome 브라우저의 TLS 지문(Fingerprint) 위장
3. **Phase 2 (내부 API 발굴)**: 웹페이지 배후의 숨겨진 데이터 주소(/api, /graphql) 자동 추적
4. **Phase 3 (헤드리스 브라우저)**: Playwright Chromium을 백그라운드에 일시 구동해 렌더링 후 캡처

## 시스템 최적화 (AG의 CLI 설계)
- **문제점**: 항상 켜두어야 하는 API 데몬 서버(FastAPI 등)는 상시 메모리(RAM)와 배터리를 점유하므로 마스터님의 맥북 시스템에 무리를 줌.
- **해결**: 해나가 이미 깔아둔 파이썬 가상환경 경로를 재활용하여, 필요할 때만 1초 실행되고 완전히 사라지는 **On-Demand CLI 공용 명령어**로 세팅.
- **경로**: `/Users/tedchanglimchangsik/.local/bin/insane-extract`
- **설정**: AG가 `chmod +x`를 통해 전체 에이전트(AG, 해나, 미모)가 터미널에서 즉시 호출할 수 있도록 실행 권한 부여 완료.

## 결과 및 테스트
- `insane-extract "https://news.ycombinator.com"` 테스트 결과, 0.17초 만에 Safari 위장을 통해 본문 추출 성공.
- 대기 메모리(RAM) 사용량: **0% (완전 소멸형)**
- 추가 비용: **$0** (오픈소스 무료 라이선스)

## 관련 문서
- [[haena]] (entity) — 해나가 최초 설치 및 venv 빌드 수행
- [[ag]] (entity) — AG가 CLI 래핑 최적화 및 권한 제어
- [[mimo]] (entity) — 미모가 필요시 CLI 호출하여 작업 예정
