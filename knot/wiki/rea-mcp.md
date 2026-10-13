---
type: entity
created: 2026-10-13
updated: 2026-10-13
sources: [https://github.com/morluto/rea]
aliases: [REA, Reverse Engineer Anything]
---

# REA MCP (Reverse Engineer Anything)

앱을 뜯어서 "이 기능은 이렇게 돌아간다"는 설계도를 주고 에이전트가 다시 만들게 하는 MCP. 통째 복사가 아니라 뜯어보고 재구현이다.

## 실측 (해나, 2026-10-13)

- 저장소 `morluto/rea`, MIT, 스타 16만대, 한국어 설명서 있음
- MCP 서버 명령: `npx -y rea-agents@6.4.0 mcp`, 손잡기(tools/list 전 initialize) 정상 응답 확인
- Hermes `mcp_servers.rea` 등록 완료. 게이트웨이 재시작 후 사용 가능
- 분석 엔진(Ghidra·Hopper·IDA) 미설치. 웹·JS 분석은 추가 설치 없이 됨

## 쓰는 법 (전 식구 공통)

- Hermes: MCP 도구로 바로 호출 (재시작 후)
- Antigravity·Claude Code·Codex: `npx rea-agents setup --client <이름>` (공식 지원)
- Hermes는 공식 미지원이라 `hermes config set mcp_servers.rea.*` 로 수동 등록했음 (2026-10-13)

## 합법선 (마스터님 확정, 2026-10-13)

- 남의 상용앱 통째 복제 금지. 뜯어서 만든 것은 강의·배포에 사용 금지, 마스터님 내부용으로만 사용
- 되는 것: 오픈소스 분석, 라이선스 보유 앱 기능 추가, 학습용, 단종 앱 살리기, 파일 형식 뜯기
- 원본 업데이트 추적 불가. 원본이 바뀌면 다시 뜯어야 함

## 관련

- ArtCraft 12종(PhotoCraft·FilmCraft 등)은 REA 주장과 연결된 오픈소스 창작 도구군. FilmCraft는 2026-10-13 실측에서 GUI만 되고 헤드리스 불가 판정, 월간 모니터 크론 등록됨 (job 필름크래프트 모니터)
- REA로 뜯을 대상은 마스터님이 지정한다. 지정 없이 뜯지 않는다
