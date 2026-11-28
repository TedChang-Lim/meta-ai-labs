---
type: concept
created: 2026-11-28
updated: 2026-11-28
sources: [hermes-ag-shared/2026-11-28_입찰-브리핑-자동운영-해나.md]
aliases: [입찰 자동운영, bidding cron, lecture/bidding]
trust: checked
---

# 새미새론 입찰·브리핑 자동 운영 (크론 3종, 토큰 0원)

나라장터 수집 → RFP 요약 → 암호화 배포 → Gemini 브리핑 수집까지 사람 손 없이 돈다. 셋 다 Hermes cron `no_agent`(스크립트만 실행)라 **LLM 토큰 0**.

| 시각 | 잡 | 스크립트 | 하는 일 |
|:--|:--|:--|:--|
| 매일 08:30 | 입찰 동기화 `a18e1cabe2e0` | `semiseron_bid_sync.sh` | 나라장터 3일치 + 포털(기업마당·NIPA·KOCCA·NIA) 수집, 대시보드 재생성 |
| 매일 09:05 | 입찰 브리핑 발행 `fe18165f6d96` | `semiseron_bid_publish.sh` | 신규 S·A 첨부 RFP 파싱 → `data/sab_extracted.json` → 대시보드 → staticrypt 암호화 → 배포 |
| 일 19:00 | Gemini 브리핑 수집 `2d7c85259cb2` | `semiseron_gemini_briefing.sh` | ego lite로 예약 스레드 읽어 새 run만 증분 저장 → 대시보드·배포 |

## 배포처와 잠금

- https://semiseron.kr/lecture/bidding/ — 저장소 `meta-ai-labs/lecture/bidding/index.html` (암호문 1개)
- 비밀번호는 **강의자료실과 동일**(키체인 `semiseron-lecture`). staticrypt@3.5.4, 골드 `#C79A51` 템플릿.
- 배포 스크립트가 ① 암호문 흔적 ② 평문 `dashboard*.html` 부재를 검사하고, 하나라도 어긋나면 배포를 멈춘다.

## 증분·중복 규칙

- Gemini 스레드는 **지연 렌더**라 보이는 run만 텍스트가 있다 → `INFINITE-SCROLLER`를 0.8화면씩 내리며 훑어 모은다.
- 중복 3겹: `_runs.json`(날짜T시각) · 본문 600자 해시 · **(날짜, 종류)** → 같은 날 브리핑은 한 건.

## 관련

- [[semiseron-bidding-strategy]]
- [[semiseron-official-naming-rule]]
