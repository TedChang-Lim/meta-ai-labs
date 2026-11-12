---
type: note
created: 2026-11-13
updated: 2026-11-13
sources: []
aliases: []
---

# 스킬 다이어트 (2026-11-13)

스킬 183개가 매 세션 컨텍스트를 잠식해 정리했다.

## 방법
- `~/.hermes/state.db` 메시지에서 `skill_view` 호출을 세어 실제 사용 기록을 뽑음
- 사용 80 / 미사용 103
- 그중 프로젝트상 곧 쓸 19개는 남기고 **84개를 서재로 이동**

## 결과
- 활성 스킬 **183 → 98**
- 보관 위치 `~/초보프로젝트/library/skills-archive/` (문서 84건 + index.html)
- 원본 폴더 `~/.hermes/skills-archive/`, 백업 `skills-backup-2026-11-13.tar.gz` (2.0MB)
- 복원 `python3 ~/.hermes/scripts/skill_restore.py <이름>`

## 규칙
새 스킬은 "매번 쓰는 절차"일 때만. 한 번 쓴 지식은 서재 문서로.

관련: [[karpathy-llm-wiki]]
