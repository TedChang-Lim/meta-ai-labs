---
type: entity
created: 2026-11-13
updated: 2026-11-13
sources: []
aliases: []
---

# 하이핏 (Hypit)

영상 구조를 **SVML**(단어 앵커 워크플로 언어)로 적어 조립·렌더하는 도구. 생성 모델 없이 자막·모션그래픽만으로도 렌더된다.

## 설치 (2026-11-13 실측)
- 스킬: `npx -y skills add hypit-ai/hypit -g` → `~/.agents/skills/hypit`
- 링크된 곳: `~/.hermes/skills`(해나), `~/.claude/skills`(코코), `~/.openclaw/skills`(루나)
- **에이지·지호·코덱스·커서·K는 링크 없음** (설치 메시지의 이름은 지원 대상 목록일 뿐)
- 본체: `npm install --global @hypit/hypit` → **0.3.2, 140MB**
- 프로젝트: `package.json`에 `"hypit": {"project": true}`
- 로컬 런타임: `hypit runtime up --runtime ./hypit.runtime.json` → chrome-headless-shell 내려받음
- 검사 `hypit check`, 빌드 `hypit build ... --follow`, 회수 `hypit get <build> --output final.video --to out.mp4`

## 0원 시연 (실측)
숏박스 설계도 8구간을 1080×1920 · 24초로 로컬 렌더. 빌드 **12초**, 산출물 298KB, 과금 0원.
- 컴포넌트: `packages/chat-scene` (TS, tsc 빌드)
- 한글 폰트: `@fontsource-variable/noto-sans-kr` (wght.css 있는 variable 패키지여야 함 — 정적 패키지는 실패)
- 캔버스 1080×1920, `fonts:Face weight=700`

## 주의
`@fontsource/*` 정적 패키지는 `wght.css`가 없어 오류. 반드시 `@fontsource-variable/*`.

관련: [[shorts-blueprint-sukbak]] · [[karpathy-llm-wiki]]
