# 🔑 API 키 종합 가이드

> 모든 API 키는 `~/.hermes/.env` 파일에 저장되어 있음.
> Hermes config.yaml의 provider 설정에서 `env:KEY_NAME` 형태로 참조됨.
> 키 값이 필요한 경우 `~/.hermes/.env` 파일에서 직접 복사할 것.

---

## 1. LLM Provider Keys

| 키 이름 | 용도 | 비고 |
|:--------|:-----|:-----|
| `OPENCODE_GO_API_KEY` | OpenCode Go (전 에이전트 주력 라우팅) | **2026.10.20 정책 개편**: 개인 API 키 체제 전환 (`Anomaly` 워크스페이스) |
| `DEEPSEEK_API_KEY` | DeepSeek V4 Flash / V4 Pro | 비상용/예비용 (직연결 종량제 사용 금지) |
| `OPENROUTER_API_KEY` | OpenRouter 라우팅 | Hy3(free) ZCode 연결용 |
| `XIAOMI_API_KEY` | MiMo 2.5 / MiMo 2.5 Pro | 비전+텍스트 모두 사용 |
| `GOOGLE_API_KEY` | Google Gemini API | Hermes 백업/fallback |
| `GEMINI_API_KEY` | Gemini (GOOGLE_API_KEY와 동일) | 통일 예정 |

> 🚨 **OpenCode Go API 키 중요 변경사항 (2026-10-20):**
> 기존 공용 서비스 계정 키가 만료되었습니다. 이제 개인 API 키를 발급받아야 합니다.
> - **발급 위치**: 계정 오른쪽 상단 메뉴 → `계정` → `개인 API 키` → `API 키 추가` (`Anomaly` 워크스페이스 선택)
> - **세부 규칙**: [opencode-go-api-key-policy-2026-10-20.md](file:///Users/tedchanglimchangsik/초보프로젝트/meta-ai-labs/knot/wiki/opencode-go-api-key-policy-2026-10-20.md) 참조

## 2. 서치/웹 Keys

| 키 이름 | 용도 | 비고 |
|:--------|:-----|:-----|
| `BRAVE_SEARCH_API_KEY` | Brave Search (1순위) | 월 1,000회 무료 |
| `TAVILY_API_KEY` | Tavily Search+Extract (2순위) | 월 1,000회 |
| `SERPER_API_KEY` | Serper 검색 (백업) | 구글 검색 |

## 3. 영상/이미지 생성 Keys

| 키 이름 | 용도 | 비고 |
|:--------|:-----|:-----|
| `KLING_ACCESS_KEY` | Kling AI 영상 생성 | 키 살아있음 |
| `KLING_SECRET_KEY` | Kling AI 시크릿 | 키 살아있음 |

## 3-1. 음성(TTS) Keys

| 키 이름 | 용도 | 비고 |
|:--------|:-----|:-----|
| `ELEVENLABS_API_KEY` | ElevenLabs TTS (한국어 캐릭터 음성) | 2026.10.24 등록 · 무료 10,000크레딧/월 · **키 파일: `~/.hermes/credentials/elevenlabs_api_key.txt`** · 무료는 비상업+출처표기 |
| `FISH_AUDIO_API_KEY` | Fish Audio TTS ("소향이" 목소리) | 무료 s2.1-pro-free · 2026-11-30까지 |

> ⚠️ **ElevenLabs 키 권한**: 키 생성 시 **Text to Speech** 권한을 반드시 켜야 한다. 꺼진 키는 모든 요청이 `401 missing_permissions`로 실패한다(실측 2026-10-24).

## 4. 커뮤니케이션 Keys

| 키 이름 | 용도 | 비고 |
|:--------|:-----|:-----|
| `TELEGRAM_BOT_TOKEN` | 텔레그램 봇 | 활성 |
| `TELEGRAM_ALLOWED_USERS` | 텔레그램 허용 사용자 | `6553511365` |
| `DAUM_EMAIL_USER` | Daum 이메일 (보고용) | `anjuman1@daum.net` |
| `DAUM_EMAIL_PASS` | Daum 이메일 앱비번 | 활성 |

## 5. 디자인/기타 Keys

| 키 이름 | 용도 | 비고 |
|:--------|:-----|:-----|
| `FIGMA_ACCESS_TOKEN` | Figma API | 디자인 연동 |
| `API_SERVER_KEY` | Hermes API 서버 인증 | 내부용 |

---

## 🔧 지호(ZCode) 연동 설정 (Hy3)

지호(ZCode Agent)에 OpenRouter + Hy3(free) 연결 완료 (2026.07.08)

```
Model Settings:
  Name:          OpenRouter
  Base URL:      https://openrouter.ai/api/v1
  API format:    Chat completions (/chat/completions)
  API key:       OPENROUTER_API_KEY (~/.hermes/.env 참조)
  Model:         tencent/hy3:free (256K context)

MCP Servers:
  - higgsfield-mcp (HTTP, 등록됨, OAuth 인증 필요)
```

## 🔧 Hermes MCP 연결 현황

```
ComfyUI FL-MCP      ✅ 연결 (108개 도구)
Voicebox (Chatterbox) ✅ 연결 (TTS)
kordoc MCP          ✅ 연결 (HWPX 문서)
korean-law-mcp      ✅ 연결 (법령 검색)
```
