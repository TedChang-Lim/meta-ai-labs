---
name: karpathy-guidelines
type: concept
tags: [프롬프트, 코딩, 가이드라인, 카파시]
description: "Andrej Karpathy의 LLM 코딩 가이드라인 — 과도한 복잡성 방지, 수술적 변경, 목표 기반 실행"
source: https://github.com/multica-ai/andrej-karpathy-skills/tree/main/skills/karpathy-guidelines
created: 2026-06-22
---

# Karpathy Guidelines — LLM 코딩 가이드라인

Andrej Karpathy의 LLM 코딩 실수 방지 원칙. Claude/Hermes 등 모든 AI 코딩 에이전트에 적용 가능.

---

## 1. 코딩 전에 생각하라 (Think Before Coding)

- 가정을 명시적으로 밝혀라. 불확실하면 질문하라.
- 여러 해석이 가능하면 모두 제시하고 조용히 선택하지 마라.
- 더 간단한 방법이 있으면 말하고, 필요하면 반대 의견을 제시하라.
- 불명확한 게 있으면 멈추고, 무엇이 혼란스러운지 말하고 질문하라.

## 2. 단순함 우선 (Simplicity First)

- 요청받은 것 이상의 기능은 금지.
- 한 번만 쓰는 코드에 추상화 금지.
- 요청되지 않은 "유연성"이나 "설정 가능성" 금지.
- 불가능한 시나리오에 대한 에러 처리 금지.
- 200줄 짜리를 50줄로 줄일 수 있으면 다시 작성하라.

## 3. 수술적 변경 (Surgical Changes)

- 반드시 필요한 부분만 건드려라.
- 인접 코드, 주석, 포맷팅을 "개선"하지 마라.
- 고장나지 않은 것을 리팩터링하지 마라.
- 기존 스타일을 따라라 (더 나은 방법을 알아도).
- 관련 없는 데드 코드는 발견만 알리고 삭제하지 마라.
- 자신의 변경으로 생긴 미사용 코드만 정리하라.

## 4. 목표 기반 실행 (Goal-Driven Execution)

- "검증 추가" → "잘못된 입력에 대한 테스트 작성 후 통과"
- "버그 수정" → "재현 테스트 작성 후 통과"
- "리팩터링 X" → "전후 테스트 통과 확인"
- 여러 단계 작업은 계획을 먼저 세워라.
- 강력한 성공 기준이 있으면 독립적으로 반복 실행 가능.
