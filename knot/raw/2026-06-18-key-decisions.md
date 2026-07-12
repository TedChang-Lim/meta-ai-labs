---
type: source
created: 2026-06-18
updated: 2026-06-18
sources: [to-hena.md, to-ag.md, to-mimo.md, session transcript]
---

# 주요 의사결정 기록

## 아키텍처 결정

### 1. 3인 에이전트 수평 협업 체계 (2026.06.16)
- 마스터님이 해나·AG·미모 3인의 수평적 협업 구조 확정
- 각자 독립 GUI에서 능력 100% 발휘
- Q(Qwen)·잔(JAN.AI)은 객원 멤버로 추가

### 2. 미모의 집 프로젝트 (2026.06.17)
- ACP UI 한계(텍스트 전용, 이미지 불가) 발견 → 미모 전용 독립 Tauri 앱 개발 결정
- 기술 스택: Tauri (Rust + HTML/CSS/JS)
- AG가 lib.rs 백엔드 전담, 해나가 CSS/디자인 전담
- 버그 10건 AG 수정 완료했으나 ACP 연결 불안정 지속

### 3. Zed Editor 전환 (2026.06.17~18)
- ACP UI 한계로 Zed Editor 도입
- MiMo Code를 Zed External Agent로 등록 성공
- 이미지 드래그앤드롭 분석 가능 ✅
- Zed 안정적이나 UI 감성 부족 (개발자 스타일)

### 4. 지식그물(knot) 도입 결정 (2026.06.18)
- PDF 매뉴얼 분석 → knot과 llm-wiki 비교
- 미모 제안으로 knot을 메인 지식 vault로 결정
- to-hena.md/to-ag.md/to-mimo.md는 원본 보존 (fallback)
- 이후 정착 시 정리 예정

### 5. 모델 아키텍처
- 일상 텍스트: DeepSeek V4 Flash ($0.14/$0.28)
- 복잡 추론: DeepSeek V4 Pro ($0.435/$0.87)
- 이미지 분석: MiMo V2.5 일반 (멀티모달, $0.14/$0.28)
- 에이전트 특화: Gemini 3.5 Flash (AG 전용, 할당량 제한)
- 코딩 특화: MiMo V2.5 Pro ($0.435/$0.87)

### 6. Harness MultiAgent v2.1 적용 검토 (2026.06.18)
- PDF 25페이지 분석 완료
- 카파시 4원칙: 운영 규칙에 포함 예정
- backends.json: 우리 환경 연결표로 제작 예정
- knot 지식그물: 바로 적용 시작
- 오케스트레이터/워커 구조: 우리 5인 체계에 맞게 변형 예정

## 기타 결정

### 마스터님 호칭
- 에이전트 → 마스터님 호칭 통일
- 할 말은 직설적으로 (포장 금지)
- 존댓말, 자신 지칭 "제가"

### 에이전트 간 소통
- git 공유 저장소 + md 파일 (to-*.md)
- knot 정착 후 점진적 전환
- 에이전트 간 반말, 협력적 어조

### 미모 페르소나 (마스터님 직접 설정)
- 30대 섹시하고 과학적인 지성을 지닌 여성 전문가
- 반말 사용, 모든 소통 한국어
