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

## OpenCode Go API — 구독 모델 직접 호출 (2026-11-06 실측)

```bash
curl -X POST https://opencode.ai/zen/go/v1/chat/completions \
  -H "Authorization: Bearer $OC_OPENCODE_GO_KEY" \
  -H "Content-Type: application/json" \
  -H "x-opencode-session: <임의 세션ID>" \
  -d '{"model":"muse-spark-1.3-contributor","messages":[...]}'
```

**세 가지를 틀리면 안 된다.** 하루를 날린 함정이다.

| 틀리면 | 증상 | 정답 |
|---|---|---|
| 엔드포인트를 `/zen/v1`로 씀 | `Insufficient account funds` (종량제 계정 조회) | **`/zen/go/v1`** (구독) |
| 모델명을 `muse-spark-1.3`으로 씀 | `Model is unavailable` | **`muse-spark-1.3-contributor`** |
| `x-opencode-session` 헤더 누락 | `MissingSessionID` | 임의 문자열이면 통과 |

**과금 확인:** 응답의 `opencode.billing_source` 가 `go` 면 **구독 차감(추가 결제 없음)**. `cost: 0` 으로 나온다.

**모델 목록 조회**

```bash
curl https://opencode.ai/zen/go/v1/models -H "Authorization: Bearer $KEY"
```

2026-11-06 기준 30종: `deepseek-v4.1-flash` `deepseek-v4-pro` `glm-5.2` `glm-5.3` `glm-5.3-flash` `grok-4.7` `muse-spark-1.2-contributor` `muse-spark-1.3-contributor` `gpt-5.6-luna` `gpt-6-luna` `claude-haiku-5-5` `hy3` `hy4` `hy4-preview` `kimi-k2.7-code` `kimi-k3` `kimi-k3.1-pro` `mimo-v2.6-flash` `mimo-v2.6-pro` `minimax-m3` `minimax-m3.1-flash` `longcat-2.0` `step-5-preview` `beam-free` `qwen3.8-max` `qwen3.8-flash` `qwen3.7-plus` `iceman-contributor-free` `gemini-4-argon` `crouton-alpha-free`

**함정** — `muse-spark-1.3` 은 추론 모델이다. 짧은 답에도 추론 토큰이 400~2,300개 나온다. `max_tokens` 를 2,000 미만으로 주면 **답이 비고 추론만 하다 끝난다.** 최소 4,000~6,000을 준다.

**함정** — 파이썬 `urllib` 으로 호출하면 403이 난다(curl은 통과). `curl --data-binary @req.json` 으로 보낸다.

- Kimi K3.1 Pro(`kimi-k3.1-pro`)는 **쓰지 않는다** — 쿼터를 급소진한다.

---

## 장부 자동 갱신

손으로 세지 않는다. 디스크를 훑어 다시 만든다.

```bash
python3 ~/.hermes/scripts/scan_installs.py
python3 ~/.hermes/scripts/build_inventory_html.py
open ~/초보프로젝트/library/install-log/index.html
```

전체 목록(141개 brew formula, 89개 폴더 등)은 위 장부에 있다. **이 페이지는 그중 "상황이 주어졌을 때 떠올려야 하는 것"만 추린 색인이다.**

## 뜯어보기 삼총사

세 가지가 역할이 다르다. 섞어 쓰면 웬만한 것은 다 뜯는다.

```
Scrapling         웹 페이지를 긁어온다 (봇 차단 우회)
REA               앱·바이너리 속을 판다 (MCP 231개 도구)
Craft Anything    뜯은 것을 바탕으로 실제 복제본을 만들고 원본과 대조해 검증한다
```

### Craft Anything

- 경로 `~/.local/opt/craft-anything/craft-anything-cli-0.5.0-macos-universal/craft-anything-cli`
- 심링크 `~/.local/bin/craft-anything-cli`
- 저장소 `storytold/craft-anything` (MIT/Apache-2.0, 100% Rust, 2026-10-31 생성)
- 설치 2026-11-08, 체크섬은 서명된 `SHA256SUMS.txt`와 대조해 통과
- 상태 `early alpha` — 미해결 이슈가 279건이다. 큰 프로젝트에 바로 쓰지 않는다

**AI는 내장돼 있지 않다.** 컴퓨터에 이미 로그인된 코딩 에이전트를 부린다.

```bash
craft-anything-cli doctor                 # 설치 상태 점검 (healthy:true 확인)
craft-anything-cli ai detect              # 쓸 수 있는 백엔드 찾기
craft-anything-cli ai add "Antigravity" --kind agent_cli --model antigravity
craft-anything-cli ai builder "Antigravity"
craft-anything-cli ai test "Antigravity"  # version_only:true 면 실제 생성은 아직 안 해본 것
```

**함정 1 — Claude Code가 `Model is unavailable`로 죽는 일이 있다.**
`~/.claude/settings.json`이 세 모델 모두 `muse-spark-1.3-contributor`로 매핑돼 있다.
2026-11-08 12:15에 craft-anything이 이 오류로 두 번 실패했다.

**그러나 이 모델은 내려간 것이 아니다.** 같은 날 15:35에 목록과 호출을 다시 확인한 결과
OpenCode Go 모델 30개 안에 그대로 있었고 `HTTP 200 · billing_source go · cost 0`으로 정상 응답했다.
**일시적 오류였다.** 모델이 사라졌다고 단정하지 말고 `GET /zen/go/v1/models`로 먼저 확인한다.

→ **Antigravity(`agy`)로 붙이면 이 오류를 피할 수 있다.** 2026-11-08 실측 통과.

**함정 2 — `--build-with` 값을 정확히 줘야 한다.** 생략하면 요청과 무관하게 Rust를 고른다.
HTML 페이지를 원했는데 `Cargo.toml`을 만드는 일이 실제로 있었다.

```
쓸 수 있는 값: Builder's choice · Electron · Next.js + TypeScript · Python
              React + TypeScript (Vite) · Plain HTML and CSS · Rust (console)
              rust · Rust + egui (eframe) · unity · unreal · godot
```

**함정 3 — `ai test`는 버전만 확인한다.** `version_only:true`로 나오면 생성 능력은 아직 검증 안 된 것이다.
실제 검증은 `rebuild` 한 번 돌려서 확인해야 한다.

```bash
craft-anything-cli rebuild - "회전하는 정육면체 단일 HTML 페이지" \
  --rounds 1 --backend "Antigravity" --unattended \
  --build-with "Plain HTML and CSS" --projects-dir <폴더>
```

**분석 모드 두 가지**

```
클린룸   겉만 본다. 화면 캡처·글자·색·배치·글꼴·여백·메뉴 반응
딥       속까지 본다. Ghidra가 깔려 있으면 연결한다 (함수 추출)
```

**선택 엔진 현황 (2026-11-08 doctor)**

```
있음    Chromium · Java · LLDB · objdump
없음    Ghidra · Frida · adb · JADX · Apktool · mitmproxy · binwalk · rizin · tshark
```

딥 모드를 제대로 쓰려면 Ghidra가 있어야 한다. Java는 이미 있으므로 바로 설치 가능하다.

## 관련

- [[scrapling]]
- [[haena]]
