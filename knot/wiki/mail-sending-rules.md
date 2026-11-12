---
type: concept
created: 2026-11-13
updated: 2026-11-13
sources: [raw/2026-11-13-mail-rules.md]
aliases: []
---

# 메일 발송 규칙

1. 보내기 전 **본문 전문과 첨부 목록**을 그대로 보여주고 "보내" 승인 후에만 발송
2. 승인본에서 문구·첨부를 바꾸지 않는다. 첨부는 지시받은 것만
3. 피클 건은 **첨부 0개** — 1장 요약도 PDF로 만들지 않고 본문 HTML 한 장이 곧 요약
4. 발송 기록은 `~/.hermes/state/mail_ledger.jsonl`에 남긴다

사고 사례: 1장 HTML만 보내라는데 10쪽 PDF를 붙여 발송. 회수 불가.

관련: [[semiseron-partners-and-mail-2026-09-27]]
