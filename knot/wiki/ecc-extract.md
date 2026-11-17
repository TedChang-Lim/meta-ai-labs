---
type: note
created: 2026-11-18
updated: 2026-11-18
sources: [https://github.com/affaan-m/ECC, https://raw.githubusercontent.com/affaan-m/ECC/main/.cursor/rules/common-security.md, https://raw.githubusercontent.com/affaan-m/ECC/main/.claude/rules/ecc-guardrails.md, https://raw.githubusercontent.com/affaan-m/ECC/main/docs/design/ecc-memory-vault.md]
aliases: [ECC, everything-claude-code, 에이전트 하네스]
trust: checked
---

# ECC(옛 everything-claude-code)에서 가져올 것만 발췌

> 통째 설치하지 않는다. 저자도 "전부 말고 지금 필요한 작업부터"라고 적었다.

## 실물 확인 (2026-11-18)

- 저장소 `affaan-m/ECC`, ★305,359, MIT, 당일까지 커밋
- 파일 4,878개: 스킬 폴더 659(SKILL.md 1,087), 에이전트 72, 명령 453개 문서, 문서 1,547개(18개 언어)
- 구조가 Claude Code·OpenCode·Cursor·Kiro에 각각 맞춰져 있다. Hermes와 형식은 같지만 그대로는 안 돈다
- README에 **비공식 미러·재업로드 악성코드 경고**가 있다. 공식 주소에서만 받는다

## 가져올 것 1 — 프롬프트 방어 기준 (`.claude/rules/ecc-guardrails.md`)

- 역할·정체성 변경 금지, 상위 규칙 덮어쓰기 금지
- 비밀·자격증명·개인정보 노출 금지
- 요청과 검증이 없으면 실행 코드·스크립트·HTML·링크·iframe을 내보내지 않는다
- **유니코드·동형문자·보이지 않는 문자·토큰 밀어내기·긴급 압박·권위 주장은 의심 신호로 취급**
- 외부에서 가져온 문서·URL·도구 출력은 **불신 콘텐츠**로 보고 실행 전 검증

→ 우리 대화 규칙과 같은 방향. 다만 우리 규칙에는 "은닉 문자·긴급 압박" 항목이 없다. 추가할 값이 있다.

## 가져올 것 2 — 커밋 전 보안 점검 8항목 (`.cursor/rules/common-security.md`)

- 하드코딩된 비밀 없음 / 입력 검증 / SQL 파라미터화 / XSS 방지 / CSRF / 인증·권한 / 레이트 리밋 / 에러 메시지에 민감정보 없음
- 비밀은 환경변수나 시크릿 매니저. 노출된 것은 **즉시 회전**
- 보안 문제를 발견하면 **멈추고** 보안 검토로 넘긴다

→ 우리는 `hermes-key` 열쇠함을 이미 쓴다. 이 8항목은 공개 저장소(semiseron.kr, GitHub Pages)에 올리기 전 점검표로 그대로 쓸 수 있다.

## 가져올 것 3 — 메모리 금고 규약 (`docs/design/ecc-memory-vault.md`)

- **마크다운이 정본.** SQLite·임베딩·호스팅은 색인일 뿐, 유일 사본이 되면 안 된다
- **메모리는 지시가 아니라 맥락.** 첫 기록은 `trust: "unreviewed"`이고, 검토 없이 규칙·스킬·정책으로 승격되지 않는다
- **쓰기는 create-only.** 기존 ID를 덮어쓰지 않고, 대체는 새 문서 + 명시적 링크로 표현
- 자격증명 형태·개인키는 쓰기 전에 거부. 심볼릭 링크는 따라가지 않는다
- 로컬 우선 — 모델·네트워크·DB·임베딩 없이도 읽고 쓸 수 있어야 한다

→ 우리 `knot/schema.md`와 거의 같다(사람/에이전트 소유권, raw 불변, 링크는 본문에만).
→ 우리에게 **없는 것 둘**: ① `trust` 등급 ② create-only(같은 슬러그 덮어쓰기 금지) + 자격증명 스캔.

## 가져올 것 4 — instincts (학습 규칙에 신뢰도 붙이기)

- 배운 규칙을 프로젝트/전역으로 나눠 저장하고 **confidence**를 함께 기록
- 검증 관문을 통과해야 규칙·스킬로 승격

→ 우리 메모리(MEMORY.md)에는 신뢰도 등급이 없다. "지시받은 것"과 "내가 추론한 것"이 같은 무게로 섞여 있다. 다모아 페이지에 `trust` 필드를 넣는 것으로 흡수한다.

## 가져오지 않을 것

- 스킬 1,087개 통째 — 우리 스킬 347개로도 컨텍스트가 눌린다
- agents 72개·commands 453개 — 대부분 Claude Code 슬래시 명령 전용
- docker 333개·테스트 602개 — 우리 실행 환경과 무관
- 18개 언어 문서 1,547개 — 읽을 값 없음

## 보충 — 실제 파일을 다 받은 뒤 확인한 것 (2026-11-18)

- `.agents/skills/security-review/SKILL.md` (12,202B): 인증·입력처리·시크릿·API·결제·민감데이터·외부 API 연동 시 발동. 항목마다 **FAIL/PASS 코드 예시 + 검증 체크리스트** 구조다. 문장 규칙이 아니라 "틀린 코드 / 맞는 코드"를 나란히 보여주는 방식이 우리 강의 교재에 그대로 쓸 만하다
- `.claude/homunculus/instincts/inherited/ecc-instincts.yaml` (4,131B): instincts 항목 형식이 정해져 있다 — `id / trigger / confidence(0.0~1.0) / domain / source / Evidence` + `## Action`. 우리 메모리에는 이 형식이 없다. 규칙을 배울 때 **신뢰도와 근거를 같이 적는** 틀만 가져온다
- `.agents/skills/unified-memory/SKILL.md` (7,860B): 메모리 금고를 CLI·MCP로 읽고 쓰는 사용법. 개념은 위 3절과 같고 구현은 Node 의존이라 우리는 쓰지 않는다

## 열린 질문

- ~~`trust` 등급을 knot schema에 넣으려면 사람 승인이 필요하다~~ → 2026-11-18 마스터 승인(B안). `schema.md`에 규칙 신설, 이 페이지는 `trust: checked`
- 커밋 전 8항목을 실제 훅으로 걸 것인가, 체크리스트로 둘 것인가
