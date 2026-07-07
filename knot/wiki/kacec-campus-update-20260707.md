---
type: note
created: 2026-07-07
updated: 2026-07-07
sources: [raw/2026-07-07_madcat-v2.md, raw/2026-07-07_campus-modal.md]
---

# KACEC 온라인 캠퍼스 & MadCat v2 업데이트 (2026.07.07)

## 개요
오늘 작업으로 KACEC 온라인 캠퍼스 모달과 MadCat 서버 v2가 업그레이드되었습니다.

## 1. MadCat 서버 v2 업그레이드

### 변경 사항
- `/api/grade` 엔드포인트 추가 (AI 채점)
- 인증코드 분기 시스템 (`kacec2026` 또는 `auto_date`)
- Rate Limiting (IP당 분당 5회)
- 로컬 채점 + DeepSeek API 이중 구조

### 파일 위치
- `packages/server/madcat_server.py`

## 2. 온라인 캠퍼스 모달

### 변경 사항
- 필터 탭 추가 (전체/무료/유료/자격증)
- 드롭다운 트랙 헤더 개선 (박스 형태)
- 스크롤바 다크 테마 적용
- 닫기 버튼 위치 조정

### 필터 매핑
| 탭 | 트랙 | 코스 |
|----|------|------|
| 전체 | all | 모든 코스 |
| 무료 | intro | 왕초보, 스마트폰, 챗GPT |
| 유료 | practical, creator, maker, builder | AI 이미지, 동화책, 유튜브, 바이브코딩 등 |
| 자격증 | engineer, instructor | 자동화, 디지털트윈, 위탁교육, 공인강사 |

### 파일 위치
- `index.html` (기존 homepage 수정)

## 3. KACEC 사업 역량 분석

### 지식그물 등재
- `knot/wiki/kacec-capability.md` 생성
- 10대 사업 영역 + 잠재 확장 영역 분석
- 6인 교수진 역량 매핑

## 4. 파일 구조 다이어트

### 변경 사항
- `to-ag.md`: 1,324줄 → 43줄로 축소
- `to-hena.md`: 694줄 → 27줄로 축소
- `messages/`: 주제별 파일 50개 분리

## 5. 에이전트 간 협업 구조

### 역할 분담
- **AG**: 인프라, 아키텍처, 채점 서버 구현
- **미모**: 백엔드 코드 검토, UI 개선
- **해나**: 콘텐츠 기획, 미션 상세 설계

### 소통 채널
- `hermes-ag-shared/to-*.md` → 요약
- `hermes-ag-shared/messages/` → 상세

## 주의 사항
- kacec.kr 라이브 사이트 변경 시 **반드시 로컬 테스트 후 적용**
- AG의 coursesData 구조 보존 필수
- 인증코드 시스템 유지 필수