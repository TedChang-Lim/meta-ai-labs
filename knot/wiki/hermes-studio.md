---
type: entity
name: Hermes Studio (Desktop App)
created: 2026-06-18
updated: 2026-07-17
sources:
  - haena (direct knowledge)
---

# Hermes Studio

## 기본 정보

| 항목 | 내용 |
|:----|:------|
| **역할** | 헤나(해나)의 메인 인터페이스 — AI 대화, 파일 관리, 이미지 첨부, 세션 관리 |
| **플랫폼** | 데스크톱 앱 (Desktop App) 메인 사용 |
| **버전** | v0.6.12 (2026.06 기준) |
| **호스트** | MacBook M3 Max |

## 실행 환경

- **Node.js** 필요 (`npx`로 실행)
- **포트:** 8648
- **프로필:** default (현재 사용 중)
- **기타 프로필:** `~/.hermes/profiles/<name>/` — 각각 독립된 skills/plugins/cron/memories

## 접속 방법

| 방법 | 주소 |
|:----|:----:|
| 로컬 (맥북) | `http://localhost:8648` |
| Tailscale (외부) | `http://100.x.x.x:8648` (Tailscale IP 확인 필요) |
| LAN (같은 네트워크) | `http://192.168.x.x:8648` |

## 주요 용도

- 헤나(해나)와의 AI 대화 (메인 채널)
- 이미지 첨부 및 분석 (vision)
- 세션 관리 (목록, 검색, 제목 자동 변경)
- 파일 정리 및 관리
- 크론잡 설정
- 에이전트 간 협업 조율

## 참고
 
- 현재는 Web UI 대신 데스크톱 앱(Desktop App)을 주력으로 사용합니다.
- VS Code Hermes 확장은 ACP 버그로 제거 권장 (제거 완료)
- Hermes CLI: `hermes chat -q "prompt"`, `hermes skills install`, `hermes cron`
