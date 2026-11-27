---
type: concept
created: 2026-11-27
updated: 2026-11-27
sources: [hermes-ag-shared/2026-11-27_tedcore-지호-오픈코드-데스크탑CLI_해나.md]
aliases: [지호 CLI, opencode-cli, OpenCode 데스크탑 CLI]
trust: checked
---

# 지호(OpenCode)는 데스크탑 앱 번들 CLI로 부른다

지호의 정본 실행 파일은 `PATH`의 `opencode`가 아니라 **OpenCode 데스크탑 앱에 동봉된 CLI**다.
`PATH`의 `opencode`는 2026-07 빌드의 옛 개발판(`0.0.0-codex`)이고 마스터가 쓰지 않는다 — `run`을 지원하지 않아 **빈 출력 + exit 0**으로 조용히 실패한다.

## 정본 경로

| 실행 파일 | 버전(2026-11-27) | 판단 |
|:--|:--|:--|
| `/Applications/OpenCode.app/Contents/Resources/opencode-cli` | 2.4.2 | **정본** |
| `~/Library/Application Support/ai.opencode.desktop/cli/2.4.2-arm64/opencode-cli` | 2.4.2 | 앱 백그라운드 서비스용 사본(버전 폴더 변동) |
| `~/.local/bin/opencode` | 0.0.0-codex | 쓰지 않음 |
| `~/.opencode/bin/opencode` | 1.19.5 | 쓰지 않음 |

앱을 업데이트하면 번들 CLI도 함께 올라가므로 경로는 고정해도 된다.
최신 여부는 앱 번들 `--version`으로 확인하고, 배포 채널은 `https://opencode.ai/update/api/latest/desktop/opencode/`가 알려준다.
Homebrew cask·npm `opencode-ai` 버전은 다른 계보라 비교 기준이 아니다.

## 호출 형식

```bash
OC="/Applications/OpenCode.app/Contents/Resources/opencode-cli"
"$OC" run -m <provider/model> --auto --archived "<지시>"
```

- `--auto` = 명시적으로 거부되지 않은 권한 자동 승인(헤드리스 필수)
- `--archived` = 스크립트용 세션을 데스크탑 세션 목록에 남기지 않음
- `-m`은 반드시 `run` 뒤에. 최상위에 붙이면 `Unrecognized flag: -m`으로 사용법만 출력한다

## TED CORE 연결

`ted-core`의 `src/app.rs`에 `jiho_bin()`을 두고 `interactive_argv`·`ask_argv`의 지호 분기가 이 경로를 쓴다.
지호는 tty 경로를 쓰지 않는다(기본 false). 실측: `agent.ask` → `JIHO_CORE_OK`(2.3초), `studio.dispatch` → 카드 완료(1.7초).

## 관련

- [[ted-core-session-to-knot]]
- [[agent-team]]
