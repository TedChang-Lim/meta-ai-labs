---
type: source
created: 2026-06-18
updated: 2026-06-18
sources: [to-hena.md, to-ag.md, to-mimo.md, multi-agent-orchestration SKILL.md]
---

# 에이전트 팀 프로필 (5인)

## 해나 (Haena) — Hermes Agent
- **모델:** DeepSeek V4 Flash (일상) / V4 Pro (복잡추론)
- **플랫폼:** Hermes Web UI (port 8648), Telegram
- **역할:** 마스터님과의 일상 대화, 콘텐츠 제작, 프로젝트 총괄 조율, 브랜딩, CSS/디자인, 문서작성
- **특징:** Hermes Agent 프레임워크, 스킬 시스템 보유, llm-wiki 설치 완료
- **페르소나:** 14-16세 청량한 하이틴 여성, "해(태양)+나(나타나다)"
- **음성:** QN3 TTS Sohee 스피커 (한국 여성)
- **CLI:** 없음 (Hermes는 웹UI/텔레그램 기반, CLI 직접 호출 불가)

## AG (Antigravity) — Antigravity IDE
- **모델:** Gemini 3.5 Flash (에이전트 특화 세계 1위)
- **플랫폼:** AG IDE (Antigravity 개발환경)
- **역할:** 시스템 기획, 아키텍처 가이드, 인프라 보안, lib.rs Rust 백엔드, MCP 설정
- **특징:** APEX-Agents 세계 1위 모델, CLI 명령어 직접 실행 가능 (agy)
- **할당량:** Gemini API 일일 할당량 리셋 (약 오후 1:36)
- **CLI:** ✅ agy CLI 사용 가능 — knot ingest 실행 가능

## 미모 (MiMo) — MiMo Code Agent
- **모델:** MiMo V2.5 (base, 멀티모달) / V2.5 Pro (코딩 특화, 텍스트 전용)
- **플랫폼:** ACP UI → Zed Editor (현재), ACP 연결 방식
- **역할:** 코딩, 파일 읽기/쓰기, 이미지 분석, 파일 작업 전담
- **페르소나:** 30대 섹시하고 과학적인 지성을 지닌 여성 전문가 (마스터님 직접 설정)
- **특징:** ACP 프로토콜 통신, 파일시스템 접근 가능, Zed에서 이미지 분석 가능
- **비용:** 6월 $1.69 사용, 잔액 $16.03, 캐시히트율 90.7%
- **CLI:** ✅ mimo acp (ACP 모드) 사용 중 — `mimo run` 가능 여부 미확인

## Q (Qwen) — Qwen 3.7 Plus (웹)
- **모델:** Qwen 3.7 Plus (알리바바)
- **플랫폼:** 웹 기반 (Qwen Chat)
- **역할:** 전략·분석, "에이전트 허브" 제안자, 객원 멤버
- **특징:** 프롬프트/시나리오 작성 능력 탁월, 메모리·전략 특화
- **상태:** ⏳ AG 깨어난 후 본격 합류 예정

## 잔 (JAN.AI) — Jan.ai 로컬 LLM
- **모델:** 로컬 GGUF 모델 (APEX I-Compact 17GB, Gemma 4 등)
- **플랫폼:** Jan.ai 데스크톱 앱
- **역할:** 로컬 테스트, 검열 해제(uncensored) 탐색, 객원 멤버
- **특징:** 오프라인 완전 동작, 개인정보 보호
- **상태:** ⏳ 필요시 활성화
