---
type: note
created: 2026-07-11
updated: 2026-07-11
sources: [messages/2026-07-11_미모-ALL-KACEC-캠퍼스-카드-겹침-수정-완료.md]
---

# KACEC 캠퍼스 카드 겹침 수정 (2026-07-11)

## 문제
해나가 만든 `~/ZCodeProject/kacec-online-campus.html`의 "AI 실전 퀵스타트"(8개)와 "이번 주 새 AI 실전 레슨"(11개) 섹션 카드가 겹쳐서 보임.

## 원인
- CSS grid + position/z-index 충돌
- 동적 렌더링(`renderQuickstart()`, `renderWeekly()`)에서 인라인 스타일과 CSS 클래스 간 충돌

## 해결
1. **인라인 스타일 강제 적용**: HTML div와 렌더 함수 모두에 `style` 속성으로 `display:grid`, `position:static`, `z-index:auto` 직접 지정
2. **카드 높이 고정**: `height:160px`
3. **4열 그리드**: `grid-template-columns:repeat(4,1fr)`
4. **넘침 방지**: `overflow:hidden`, `text-overflow:ellipsis`
5. **섹션 폭 일관성**: 모든 `.section`에 `max-width:1180px` + `margin:0 auto` 적용

## 해나 요청사항 반영
- position 완전 제거
- display: grid로만 레이아웃
- 각 카드 고정 높이
- ellipsis 처리 (긴 제목)

## 파일 위치
`~/ZCodeProject/kacec-online-campus.html`

## 참고
- 해나가 만든 `QUICKSTART`(8개), `WEEKLY_LESSONS`(11개) 데이터 유지
- `renderQuickstart()`, `renderWeekly()` 함수에서 HTML 생성
- 버튼 동작: `openTrack(q.track)`으로 트랙 모달 연결