# 🔑 API 키 종합 가이드

> 모든 API 키는 `~/.hermes/.env` 파일에 저장되어 있음.
> Hermes config.yaml의 provider 설정에서 `env:KEY_NAME` 형태로 참조됨.
> 키 값이 필요한 경우 `~/.hermes/.env` 파일에서 직접 복사할 것.

---

## 1. LLM Provider Keys

| 키 이름 | 용도 | 비고 |
|:--------|:-----|:-----|
| `DEEPSEEK_API_KEY` | DeepSeek V4 Flash / V4 Pro | Hermes 메인 provider (직연결) |
| `OPENROUTER_API_KEY` | OpenRouter 라우팅 | Hy3(free) ZCode 연결용 |
| `XIAOMI_API_KEY` | MiMo 2.5 / MiMo 2.5 Pro | 비전+텍스트 모두 사용 |
| `GOOGLE_API_KEY` | Google Gemini API | Hermes 백업/fallback |
| `GEMINI_API_KEY` | Gemini (GOOGLE_API_KEY와 동일) | 통일 예정 |

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
