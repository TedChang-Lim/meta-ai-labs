---
type: note
created: 2026-09-28
updated: 2026-09-28
sources:
  - https://github.com/VelornLabs/velorn
  - https://github.com/KyaniteLabs/kinocut
aliases: [Velorn 검증, AI 에이전트 영상편집 도구 선별, GUI 의존 도구 걸러내기]
---

# Velorn 실측 검증 — 도구 소개문과 실제 능력의 간극

## 왜 이 기록을 남기나

에이전트 도구를 **소개문만 보고 고르면 안 된다**는 것을 실측으로 증명한다.
2026-09-28 밤, 마스터님 요청으로 AI 에이전트가 영상편집을 대리할 수 있는 무료 도구를 찾던 중 생긴 기록이다.
강의·책의 "실제 검증" 사례素材로 쓰인다.

## 결론 한 줄

**도구의 도구 수와 MCP 지원 개수는 능력이 아니다. 실행이 에이전트에게 열려 있는지가 능력이다.**

## Velorn 실측 결과

### 설치 (성공)

| 항목 | 값 |
|---|---|
| 저장소 | VelornLabs/velorn, GPL-3.0, 491 star |
| 버전 | v0.3.36 (2026-09-26 배포) |
| 파일 | Velorn-0.3.36-mac-arm64.dmg, 326MB |
| sha256 | `f6869f1e…01cb26d` — GitHub 공식값과 일치 |
| 서명 | Developer ID (Jaime Aguirre, 4T66ZQ5AC3) + 공증 티켓 첨부 |

악성코드가 아니었다. 서명·무결성은 문제없었다.

### MCP 접속 (성공)

- 로컬 MCP 서버 `http://127.0.0.1:19790/mcp` 개방
- **도구 130개** 확인, 95개에 `previewOnly` 안전장치
- Hermes에 `mcp_servers.velorn`으로 정식 등록

### 편집 실행 — 여기서 벽 (핵심)

Velorn은 **130개 MCP 도구가 전부 앱 화면(렌더러)을 클릭하는 명령**이었다.

증거:
1. 창 크기 1600×1000인데 렌더러 실제 렌더 크기 **0×0**
2. 앱 내부 백엔드 `TypeError: Failed to fetch` **367회** 반복 (무한 재시도 루프)
3. `create_project` → `Timed out waiting for Velorn to apply MCP action`
4. MCP 응답이 `"Background process started"`라는 **비도구성 텍스트**로 도달

창을 사람이 띄우면 풀렸다. 이후 실제 조작 성공:
- 촬영본 `편집본/#3.mp4` 75MB 임포트 성공
- 타임라인 배치 성공 (영상 + 음성 클립 자동 분리)
- `trim_clips` 5초→3초 **실제 반영**, `project.comfystudio`에 `"duration": 3` 저장 확인
- `export_timeline` → mp4 생성 (1920×1080 H.264 + AAC, 2.8MB)

즉 **사람이 창을 띄우면 된다**. 문제는 "창 없이는 못 한다"는 점이다.

### 진짜 한계 — 자막

`transcribe_captions` 실패:
```
"error": "The local caption engine is not installed."
```

Velorn 안의 자막 엔진은 별도 설치가 필요하다. 마스터님 맥에 이미 있는 faster-whisper를 못 쓴다.
**청각장애인 영화에 자막이 필수인데 그 부분을 제공하지 못한다.** 이 프로젝트에 결정적인 결함이다.

### 프로그램 정체 (마스터님 질문에 대한 답)

- **유료인가**: 앱은 GPL-3.0 무료. 계정·구독 없음.
- **왜 무료 배포인가**: 앱은 무료, 돈은 **제너레이션**에서. 공식 README에 cloud workflow 예시가 `Nano Banana 2, GPT Image 2, Seedance, Kling` 라고 명시.
- **화면의 템플릿/SS는 무엇인가**: Velorn 기능이 **아니다**. ComfyUI 공식 템플릿 카탈로그(500개+)를 임베드해 보여주는 창. ComfyUI가 꺼져 있으면 전부 비어 있다.
- **Velorn의 정체**: ComfyUI 위의 **생산 계층**. "Velorn is not a replacement for ComfyUI. It is the production layer around ComfyUI." 편집기가 아니라 AI가 재료를 만들어준 뒤 매립하는 껍데기.
- **생성 기능 비용**: ComfyUI 필요 → GPU 전기값. 편집·자막·내보내기는 ComfyUI 없이 동작.

### 내가 잘못한 것 두 가지

1. **도구 목록만 보고 1순위로 추천했다.** 130개 도구와 "MCP" 문구를 읽고 "에이전트가 편집 가능하다"고 결론 내렸다. 실행이 GUI 클릭이라는 점을 미리 의심하지 않았다.
2. **Velorn이 무의미하다고 단정했다.** "GUI 의존이니 쓸 수 없다"고 말했으나, 사람이 창을 띄우면 실제 편집이 된다. 정확한 표현은 "창 없이는 못 한다"다. 제가 백그라운드에서 밀어붙인 탓에 잘못 판단했다.

## 일반화 — teaches (에이전트 도구 선별 기준)

1. **도구 수가 능력이 아니다.** Velorn 130개, kinocut 201개. 실행 경로가 핵심이다.
2. **MCP를 붙였다고 에이전트용이 아니다.** Velorn도 MCP 서버를 제공했다. 하지만 그 명령은 창 클릭이다.
3. **창(UI) 의존 도구는 에이전트 자동화의 벽이다.** 사람 대리 조종이 목적이면 쓸 수 있다. 자동화가 목적이면 버린다.
4. **요구사항을 도구가 못 채우면 그게 결함이다.** 청각장애인 영화에 자막 필수인데 Velorn 자막 엔진을 안 태우는 순간, 이 프로젝트에서 탈락이다.
5. **추천 전 실측이 전제여야 한다.** 이번 교훈의 출발점이자 결론이다. "될 것 같다"가 아니라 "돌려봤다"가 기준이다.

## 대안 — kinocut (차기 후보)

| | Velorn | kinocut |
|---|---|---|
| 라이선스 | GPL-3.0 | **Apache-2.0** (상업 사용 가능) |
| 구조 | GUI 클릭 | **ffmpeg 직접 생성** |
| 창 필요 | **필요** | **없음** |
| 도구 수 | 130 | 201 (MCP) + 173 (CLI) |
| 자막 | 엔진 미설치로 실패 | `video_ai_transcribe` + `video_subtitles_styled` |
| 인트로 제작 | HTML 임베드(18 도구) | Hyperframes 내장 |
| 성숙도 | v0.3.36, star 491 | v1.15.2 (2026-09-24), star 175 |
| 갱신 | 6일 전 | **6시간 전** |

**아직 실측 안 했다.** 이 페이지는 추천이 아니라 관찰이다.
실측 결과는 [[kinocut-verification-2026-09-28]] 에 남긴다.

## 사업 구조에서 본 교훈

Velorn은 **무료 편집 도구 + 유료 생성** 구조다. 앱을 무료로 주고 생성 단계에서 과금한다.
도구 선택의 문제가 아니라 **사업 구조의 문제**다. 마스터님이 "무료에 가깝게"를 조건으로 삼은 이유가 여기서 분명해진다 — 편집 도구는 무료로 뿌리고, AI가 재료를 만드는 쪽에서 돈을 번다.

## 관련

- [[ai-video-pipeline]]
- [[master-projects]]
- [[kinocut-verification-2026-09-28]] <!-- stub -->
