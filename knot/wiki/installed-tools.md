---
type: entity
created: 2026-11-06
updated: 2026-11-06
sources: []
aliases: [도구 대장, tool ledger, 설치 도구]
---

# 이 맥에 깔린 도구 대장 — 모든 에이전트 공용

**이 페이지가 도구 존재 여부의 유일 정본이다.** 새 도구를 깔았으면 여기에 경로와 용도를 적는다. 적지 않으면 다음 세션은 그 도구가 없는 줄 알고 헛수고한다.

## 왜 이 페이지가 필요한가

2026-11-06, Scrapling이 이미 설치돼 있었는데 "우리 원래 깔려 있지 않아?"라는 질문을 받고서야 확인했다. 설치 위치가 `~/.hermes/hermes-agent/venv/bin/` 안쪽이라 PATH에 없었고, 어떤 문서에도 실제 경로가 적혀 있지 않았다. **문서만 있고 실물 기록이 없으면 없는 것과 같다.**

## 철칙

1. **도구를 깔면 이 페이지에 먼저 적는다.** 경로·버전·용도·호출법 네 가지를 채운다.
2. **"없다"고 답하기 전에 이 페이지를 본다.** 없으면 아래 세 줄로 디스크를 먼저 뒤진다.
   ```bash
   which <이름>
   mdfind -name "<이름>" | head -20
   find ~ -maxdepth 5 -iname "*<이름>*" -not -path "*/Library/*" 2>/dev/null | head -20
   ```
3. **venv·uv·npm 안쪽에 깔린 것은 PATH에 없다.** 반드시 껍데기(symlink)를 `~/.local/bin`에 만들어 PATH에 노출한다.

---

## 문제 → 도구 (먼저 이 표를 본다)

| 막힌 상황 | 쓸 도구 | 호출 |
|---|---|---|
| 사이트가 봇 차단(403·Cloudflare) | **Scrapling** | `scrapling` |
| 데스크톱 앱을 AI가 눌러야 함 | **agent-desktop** | `agent-desktop` |
| AI 에이전트 여러 개를 한 화면에서 | **Herdr** | `herdr` |
| 폰에서 허더 조작 | **Ovis** (앱) | `/Applications/Ovis.app` |
| 로그인 필요한 사이트 크롤링 | **Aside** | `aside` |
| 영상 자르기·합치기·변환 | **ffmpeg** | `/opt/homebrew/bin/ffmpeg` |
| 유튜브 자막·영상 받기 | **yt-dlp** | `yt-dlp` |
| 긴 음성 전사 | **mlx_whisper** | `/usr/bin/python3 -c "import mlx_whisper…"` |
| 맥↔폰 원격 연결 | **Tailscale** | `tailscale` |
| 한글 문서 조판·HWPX | **rhwp** | `rhwp` |
| 오피스 문서 생성 | **officecli** | `officecli` |

---

## 실측 경로 (2026-11-06 확인)

### 수집·자동화

- **Scrapling 0.5** — `~/.local/bin/scrapling` → 실제 본체 `~/.hermes/hermes-agent/venv/bin/scrapling`
  - TLS 지문 위장(curl_cffi)이라 헤드리스 크롬처럼 차단되지 않는다. 상세는 [[scrapling]]
  - 도우미: patchright 1.64.4 · playwright 1.64.1 · curl_cffi 0.17.0 (같은 venv)
- **agent-desktop 1.2.0** — `/opt/homebrew/bin/agent-desktop` (brew)
  - 접근성 트리로 데스크톱 앱을 읽고 `@ref`로 클릭·입력. 스크린샷 픽셀 매칭 없음
  - macOS 권한 3종 승인 완료(접근성·자동화·화면기록)
  - **실측 한계:** 창 단위 읽기는 이 맥에서 대부분 실패(`not exposed through accessibility`). 메뉴바·독 표면은 정상. 창을 주 모니터로 옮기거나 `--force-renderer-accessibility`로 띄워야 한다
- **Aside** — `~/.local/bin/aside` (로그인 세션 유지 브라우저)
- **yt-dlp 2026.08.19** — `/opt/homebrew/bin/yt-dlp`
- **ffmpeg / ffprobe 8.1.2** — `/opt/homebrew/bin/` 에만 있다. `/usr/bin/ffmpeg`는 **없다**

### 에이전트 편대

- **Herdr 0.9.5** — `/opt/homebrew/bin/herdr` · 서버 `~/.config/herdr/herdr.sock`
  - 앱: `/Applications/Herdr.app` (herdr-core가 실제 실행, 앱은 화면)
  - 원격: `herdr --remote <ssh-target>` / 헤드리스: `herdr server`
- **Ovis** — `/Applications/Ovis.app`. 허더의 폰·웹 클라이언트 (구 herdr web UI)
- **Tailscale** — `/usr/local/bin/tailscale`. 이 맥 `100.66.67.89`

### 문서

- **rhwp** — `~/.local/bin/rhwp`
- **officecli** — `~/.local/bin/officecli`
- **kordoc** — PATH에 없다. MCP(`mcp__kordoc__*`)로만 호출

### 런타임

- `node` · `npx` · `bun` · `uv` 모두 `~/.local/bin`

---

## 장부 자동 갱신

손으로 세지 않는다. 디스크를 훑어 다시 만든다.

```bash
python3 ~/.hermes/scripts/scan_installs.py
python3 ~/.hermes/scripts/build_inventory_html.py
open ~/초보프로젝트/library/install-log/index.html
```

전체 목록(141개 brew formula, 89개 폴더 등)은 위 장부에 있다. **이 페이지는 그중 "상황이 주어졌을 때 떠올려야 하는 것"만 추린 색인이다.**

## 관련

- [[scrapling]]
- [[haena]]
