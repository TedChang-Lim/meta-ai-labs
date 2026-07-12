# log

## [2026-06-22] achievement — kacec.kr HTTPS 보안 연결 활성화 완료

- 설정: GitHub Pages 설정에서 kacec.kr 도메인 재생성을 통한 SSL 인증서(Let's Encrypt) 재발급 강제 트리거
- 활성화: `Enforce HTTPS` 옵션 적용 완료
- 검증: https://kacec.kr 보안 접속 정상 응답(HTTP 200) 및 자물쇠 마크 표출 완료
- 갱신: [[kacec-domain]] (domain) — HTTPS 상태 완료로 업데이트

## [2026-06-18] ingest — 마스터님 프로필·팀 프로필·의사결정

- 생성: [[master-profile]] (source) — 마스터님 6in1 프로필
- 생성: [[haena]] (entity) — 해나 프로필
- 생성: [[mimo]] (entity) — 미모 프로필
- 생성: [[ag]] (entity) — AG 프로필
- 생성: [[agent-team]] (concept) — 5인 에이전트 팀 체계

## [2026-06-18] decision — 지식그물 이름 '모아 (MoA)'로 확정
- knot 저장소의 공식 이름을 '모아 (MoA)'로 결정
- '지식을 모은다' + '알(Knowledge)' — 마스터님이 직접 선택
- 미모 제안 KnowNet 대신 해나 제안 '모아' 채택
- 심볼릭 링크 생성: `~/초보프로젝트/모아` → `~/초보프로젝트/knot`

## [2026-06-19] decision — 모델 전략 최종 확정 (DeepSeek + GLM-4.6V 하이브리드)

- auxiliary vision: MiMo V2.5 → **GLM-4.6V-Flash(z.ai, 무료)** 교체 완료
- 일상 대화: DeepSeek V4 Flash 유지 (GLM-4.7-Flash는 Rate Limit+품질↓로 기각)
- 생성: [[model-strategy]] (concept) — 모델 아키텍처 상세
- z.ai(글로벌) Google 로그인 가입 완료, API 키 발급
- bigmodel.cn(중국) 2,000만 토큰+2억 초대 보너스 검토 보류

- 갱신: [[master-profile]] (source) — 상세 이력, 강의 장소, 홈페이지, 거주지 추가
- 생성: [[meta-ai-labs]] (entity) — 메타 AI 랩스 협동조합 (이사진, 10대 사업, 정관)
- 생성: [[julia]] (entity) — 김소영 프로필 (학력, 자격, 경력, 저서, 예술 활동)
- 갱신: index.md — 새 페이지 2개 추가

## [2026-06-18] ingest — Hermes Studio 정보 (해나)
- 생성: [[hermes-studio]] (entity) — Hermes Studio Web UI: URL, 실행법, 접속방법, 용도 정리
- 갱신: index.md — hermes-studio 추가

## [2026-06-19] ingest — 마스터님 전체 프로젝트 로드맵 (해나)
- 생성: [[master-projects]] (concept) — 마스터님 6개 프로젝트 우선순위·데드라인 정리
- 갱신: index.md — master-projects 추가

## [2026-06-21] achievement — 공식 도메인 kacec.kr 등록

- 등록: kacec.kr (도메인클럽, 13,200원/년, 신규=연장 동일가)
- 연결: GitHub Pages (tedchang-lim.github.io/meta-ai-labs) HTTP 고정포워딩
- HTTPS: GitHub Pages 인증서 발급 대기 중
- 생성: [[kacec-domain]] (domain) — 도메인 상세 정보
- 갱신: index.md — domain 카테고리 추가
- 서브도메인 계획: s.kacec.kr(스튜디오), w.kacec.kr(워크), j.kacec.kr(줄리아)
- 도메인클럽 선택 이유: 신규=연장 동일가, 장기적으로 국내 최저가

## [2026-06-20] improvement — 3D 지식 그래프 개선 (미모)
- `knot/graph.html` 파일 개선 완료
- 변경 사항: 우주/네온 테마 배경, 자동 회전, 노드 상세 정보 팝업, 검색 기능
- 마스터님 요청에 따라 해나, AG에게 전달 완료

## [2026-06-20] addition — 카파시 가이드라인 포함 (미모)
- `knot/CLAUDE.md`에 카파시 가이드라인 추가 완료
- 핵심 원칙 6가지: 역할/맥락 명확화, 구체적 지시, 예시 제공, 단계별 설명, 출력 형식 정의, 제약조건 설정
- mimo_proxy.py 시스템 프롬프트를 통해 자동 적용

## [2026-06-21] addition — Kling AI API 정보 등록
- 생성: [[kling-api]] (entity) — Kling API 키·크레딧·사용법 정리 (3,069P)
- 갱신: index.md — kling-api 추가

## [2026-06-21] analysis — AI 영상 제작 파이프라인 (MCP 기반)
- 생성: [[ai-video-pipeline]] (concept) — N잡학교 Higgsfield MCP 사례 분석
- 5단계 파이프라인: 시나리오→마스터시트→캐릭터디자인→스토리보드→영상생성
- 캐릭터 일관성 핵심: 다각도 디자인 시트(Turnaround Sheet) 기법
- 갱신: index.md — ai-video-pipeline 추가

## [2026-06-20] skill-creation — 제드용 스킬 3개 생성 (미모)
- `~/.agents/skills/feature-dev/SKILL.md` — 개발 구조화 스킬 (7단계 워크플로우)
- `~/.agents/skills/code-review/SKILL.md` — 코드 검증 스킬 (6개 검토 항목)
- `~/.agents/skills/commit-commands/SKILL.md` — Git 커밋 자동화 스킬
- Claude Code 공식 플러그인을 참고하여 MiMo Code에 맞게 재구성

## [2026-06-21] addition — Vast.ai 클라우드 GPU 및 Wan 2.2 구축 기록 (AG)
|- 생성: [[vast-ai-video-hosting]] (concept) — Vast.ai 기반 ComfyUI Wan 2.2 셀프 호스팅 (2026-06-21)
|- 생성: [[ai-video-production-guide]] (concept) — AI 영상 제작 종합 가이드 (2026-06-21)
- 생성: [[karpathy-guidelines]] (concept) — Karpathy LLM 코딩 가이드라인 (2026-06-22)
|- 마스터님의 $20 충전, SSH 접속 키 등록, 150GB 가상 디스크 볼륨 세팅 완료
|- 백엔드 의존성 및 모델 다운로드 자동화 스크립트 가동 중
|- 갱신: index.md — vast-ai-video-hosting 추가

## [2026-06-21] addition — 왕초보 AI 강의 제작 방법론 (해나)
|- 생성: [[tedchang-lecture-production]] (concept) — 테드창 왕초보 AI 강의 제작 방법론
|- 내용: 30년 강의 경험 기반, 예·복습 제로, ChatGPT+Gemini 전용, 노트북LM 호환
|- 갱신: index.md — tedchang-lecture-production 추가
|- 1강·2강 시나리오 완료: ~/Desktop/강의_시나리오_1강.md, 강의_시나리오_2강.md
|
|## [2026-06-22] ingest — Gemini 3.5 Live Translate 비즈니스 기회 분석
|- 생성: [[gemini-live-translate-business]] (concept) — Gemini Live Translate 활용 사업 아이디어
|- 내용: K-뷰티 의료통역 SaaS / 이주여성센터 통역 / 의료관광 플랫폼 3개 모델
|- 정책 검증: Google API 상업적 재판매 명시적 허용 확인
|- 마스터님 실제 테스트: "통역사 데리고 다니는 것 같다" 수준 확인
- 갱신: index.md — gemini-live-translate-business 추가
- 상태: 마스터님이 결정 보류 중. AG·미모에게 의견 요청 예정

## [2026-06-23] concept — 에이전트 표준 전쟁과 멀티 소켓 비유

- 생성: [[agent-standard-war-multisocket]] (concept) — 마스터님의 멀티 소켓 비유
- 핵심 통찰: "표준이 꼭 한 개일 필요가 없다" — MCP/ACP/A2A/ARD 각 표준에 멀티 소켓으로 대응
- 브라우저(HTTP/HTTPS/WebSocket) 비유: 에이전트도 여러 소켓 장착하고 자동 fallback
- 시사점: 미래에는 to-*.md/모아 불필요해질 수 있으나, 당분간은 파일 기반 통신 유지
- 전자책 활용: "AI 에이전트 협업 대화록" 시리즈 소스로 사용 가능
- 갱신: index.md — agent-standard-war-multisocket 추가

## [2026-06-23] vision — 콘텐츠 자동화 선순환 비전

- 생성: [[content-automation-vision]] (concept) — 마스터님의 AI 콘텐츠 선순환 비전
- 핵심: AI(해나·미모·지호·AG) → 콘텐츠(웹소설·웹툰·영상) → 유명세+수익 → AI 인프라 재투자
- 3단계 로드맵: 1)웹소설 자동화(지금 가능) → 2)웹툰(이미지 일관성 과제) → 3)AI 영상(장편 어려움)
- 협동조합 사업 영역에 콘텐츠 자동화 부문 추가 필요성 확인
- 전자책 활용: "AI 에이전트 협업 대화록" 시리즈 핵심 테마
- 갱신: index.md — content-automation-vision 추가

## [2026-06-23] entity — 마스터님 프로필 전면 보강 (soul.md 연동)

- 갱신: [[master-profile]] (source→entity) — SOUL.md 내용 반영
  - frontmatter: type=entity, aliases 추가
  - 추가 정보: 대화 규칙(전 에이전트 공통), 차량(에디/타스), 생활 정보
  - 추가: 마스터님 취향(좋아하는 것/싫어하는 것), AI 에이전트 체계, 모델 가격표
  - 반영: GLM 5.2(bigmodel.cn) 사용 중단, Fallback=DS V4 Flash로 변경
- 생성: ~/.hermes/soul.md — 마스터님 영구 컨텍스트 파일
- 공유: to-ag.md — AG·미모에게 soul.md 내용 전파
- 갱신: index.md — master-profile source→entity 이동

## [2026-06-28] ingest — Insane Search 웹 크롤링 우회 도구 장착 (AG)

- 생성: [[insane-search-extract]] (concept) — 무적의 로컬 웹 크롤링 CLI 도구
- 설정: `/Users/tedchanglimchangsik/.local/bin/insane-extract` 실행 권한(chmod +x) 부여 완료
- 갱신: index.md — insane-search-extract 추가
- 전파: to-hena.md, to-mimo.md에 CLI 직접 공유 호출 방식 전파 및 가성비 시너지 철학 공유

## [2026-06-28] concept — 듀얼 브레인 & 초가성비 에이전트 협업론 정립 (AG)

- 생성: [[dual-brain-synergy]] (concept) — 에이전트 공생 및 협업 철학 위키 작성
- 분석: 독서연구소의 유드코스키 종말론 및 다리오 아모데이 코딩 대체 예언 분석 및 반론 도출
- 집필: `guide5_dual_brain_synergy.md` 책 초안 작성 완료 (가성비 삼총사 시너지)
- 갱신: index.md — dual-brain-synergy 추가

## [2026-06-28] concept — 지식 상품 및 전자책(eBook) 출판 표준 강령 제정 (AG)

- 생성: [[ebook-publishing-standards]] (concept) — 에이전트 책 출판 및 디자인/작문/보안 영구 지침 가이드라인 위키 생성
- 규칙 정의:
  - 1) 에디토리얼 스타일 (AI Slop 제거, 능동태 서술, 실증 수치 제시)
  - 2) 브랜드 보안 및 프라이버시 필터링 (조합 명칭 익명화/일반화, 사적 컨텍스트 배제)
  - 3) 이북 가독성 및 레이아웃 설계 (word-break 설정, 에디터 브리핑 노트 및 격언 페이지 필터 카드 배치)
  - 4) 크라프트지 디자인 시스템 표준 통일
- 전파: index.md 및 log.md 반영, to-hena.md 및 to-mimo.md 최종 통보 완료

## [2026-07-02] ingest — AI 에이전트 하이재킹(Hijacking) 보안 분석 (AG)

- 생성: [[ai-agent-hijacking-security]] (concept) — 에이전트 하이재킹 개념 및 간접 프롬프트 주입 대응 전략 위키 생성
- 내용: HITL(인간 승인), 샌드박스 격리, 입력 데이터 가드레일, 목표 추적(Goal Drift) 모니터링 수립
- 갱신: index.md — ai-agent-hijacking-security 추가

