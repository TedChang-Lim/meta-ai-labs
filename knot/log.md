# log

## [2026-10-24] investigate — kordoc 4.24.1 현황·융합 판단

- 생성: [[kordoc-4.24-fusion]] (entity) — 파서가 HWPX 생성까지 확장. 서식 견본 승계(4.23.0)·예산 검산·블록 검수(4.24.0)
- 실측: 보고서 생성 73,812B / 왕복 재파싱 정상 / 학위논문 51,013자·표 121행 / 졸업계획서 견본 승계 9,289B / SVG 렌더 정상
- 판단: 재구현하지 않고 kordoc을 축으로. 우리는 내용·한컴 실물 검수에 집중
- 다음: 맥북에서 `--template` 재생성 → 한컴 육안 확인 → 예산 검산 연결
- 미확인: 한컴오피스 실물 뷰어에서 열어본 것은 아님

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

## [2026-07-18] achievement — KACEC 공식 홈페이지 개편 및 모바일 사용성 극대화 (AG)

- 갱신: KACEC 이사진 프로필 슬림화 (임창식 이사 6개 태그, 한기열 이사 5개 태그 변경)
- 추가: 김소영 이사장 & 임창식 이사 2026년 2학기 대학/지자체 출강 일정 (상지대 평생교육원 및 원주시 학습관) 테이블 통합 이식
- 추가: 신규 강좌 '청소년 종이회로 메이커' (15번째) 단과 개설 및 교구재 연계 (위계 정렬 순서를 미디어아트 바로 뒤로 조정)
- 추가: 정식 통과된 정관 전문 아코디언 뷰어 탑재 및 실시간 배포
- 개선: 모바일 기기에서의 슬라이딩 햄버거 메뉴(사이드바 서랍 ☰) 구축 및 헤더 여백 조정
- 버그수정: 모바일 메인 히어로 영역의 가로 오버플로우로 인한 뷰포트 강제 줌아웃 현상 해결 (버튼 세로 배치)
- 전파: to-hena.md, to-mimo.md 공유 및 Wiki log 반영 완료

## [2026-09-27] note — 새미새론 협약 페이지 신설·홈페이지 연결·메일 라우팅 켜짐 (해나)

- 배포: `partners.html` 신설 — 협약 기관 2곳(원주영상미디어센터 9. 17. · 흥업면 주민자치위원회 9. 16.), 커밋 81d770a main 푸시, 라이브 200 확인
- 홈페이지: 상단 메뉴에 MOU 한 줄, AI LABS 다음 문의 앞에 "함께하기로 한 기관" 띠 추가
- 상단 배경: 협약 사진을 걷어내고 코드로 그린 점·선 그림으로 (마스터님이 시안 3안 선택). 협약 사진은 사실 기록이므로 배경으로 누르지 않고 카드 안 원래 밝기 그대로
- 메일: semiseron.kr 클라우드플레어 메일 라우팅 켜짐 — DNS 5레코드 삽입, 주소 7개 생성, 시험 수신 4건 도착 확인. 에이지가 남겨 둔 라우팅 켜기·레코드 삽입 누락분을 채운 것
- 되돌리기: `git revert 81d770a` · 넣기 전 원본은 `~/.hermes/cache/scratch/` 에 남김
- 접음: 사진 얼굴·몸매 보정(마스터님 판단). 미룸: 이사 4명 메일 주소(금요일 이후 — 확인 메일이 사전 통보 없이 가므로)
- 상세: [[semiseron-partners-and-mail-2026-09-27]]

## [2026-09-28] note — Velorn 실측 검증 + 에이전트 도구 선별 스킬 신설 (해나)

- 계기: 마스터님, "에이전트가 쓸 수 있는 무료 영상편집 도구"를 찾게 되심. AI 에이전트가 242개 클립을 자동 편집할 수 있을 것이라 함
- Velorn 설치: v0.3.36 Mac Apple Silicon, sha256 GitHub 공식값 일치, Developer ID + 공증 첨부 확인
- Velorn 실측: MCP 127.0.0.1:19790, 도구 130개(95개에 미리보기). 사람이 창을 띄우면 실제 편집 성공 — 촬영본 75MB 임포트, 타임라인 배치(영상+음성 자동 분리), 5초→3초 자르기 반영(`"duration": 3` 디스크 저장 확인), mp4 내보내기(1920×1080 H.264+AAC 2.8MB)
- **핵심 발견**: 130개 도구 전부가 앱 화면 클릭 명령. 창 없이는 모든 쓰기 명령이 타임아웃. 창 1600×1000인데 렌더러 0×0, 백엔드 `Failed to fetch` 367회
- **탈락 사유**: 자막 엔진 미설치(`The local caption engine is not installed.`). 청각장애인 영화에 자막이 필수인데 그 부분을 제공하지 못함
- 대안 후보: kinocut(Apache-2.0, 201 도구, ffmpeg 직접 호출, 창 불필요, Hyperframes로 HTML 인트로 제작 가능). star 175·6시간 전 갱신. **아직 실측 안 함**
- 순서 교정: 마스터님 지적 — "Velorn은 니가 쓰는 거고 나는 필모라를 쓰면 된다". 도구 선택 기준에서 빠졌던 원칙. 사람 대리 조종 도구인지, 에이전트 자동화 도구인지를 먼저 물어야 함
- 정리: 오늘 밤 만든 Velorn 테스트 프로젝트(75MB)·임시 프레임 6장·설치 dmg 전부 제거. 영화 폴더는 원본 4개만 남음
- 산출물: `wiki/velorn-verification-2026-09-28.md`, 스킬 `verify-before-recommending-agent-tools` 신설
- 미커밋: 이 실행 시작 시 `wiki/master-profile.md`·`wiki/semiseron_v12_orchestration_casestudy.md` 수정분과 `wiki/agent-mindset.md`·`wiki/semiseron-official-naming-rule.md`·`../semiseron_v12.html` 신규 파일이 이미 미커밋 상태였다. schema.md 규약(실행 시작 시 working tree가 더러우면 중단하고 보고)에 따라 커밋하지 않고 남긴다
- 상세: [[velorn-verification-2026-09-28]]




## [2026-10-13] query — HWPX 커뮤니티 현황과 판 비교 측정

rhwp 0.8.6·0.8.7 비교로 글자 수 6,582자 동일·쪽 수 37 vs 31 측정. 학위논문 Ⅱ장·실험계획서 1.4절 반영.

## [2026-10-13] query — REA MCP 등록과 합법선 확정

morluto/rea(MIT, 스타 16만) Hermes mcp_servers.rea 수동 등록·손잡기 확인. 분석 엔진 미설치. 합법선: 통째 복제 금지·내부용만. 상세: [[rea-mcp]]

## [2026-10-23] update — HWPX 커뮤니티 10일 뒤 재조회와 원고 반영

rhwp 별 3,919→3,989(공개판 v0.8.7 그대로, 기본 가지에서 10/20~22 조판 결함 6건 종결) · kordoc v4.21.27→v4.24.1 · alhangeul 0.2.3 · hanji v0.5.0 신규. 학위논문 표 4·2.3·2.4절 갱신, 판 비교 40/34·11/10. 표 뒤 빈 줄을 지워 실험계획서 12→11쪽. hanji는 rhwp를 품고 있어 편차 측정 표본에서 제외. 상세: [[hwpx-community-2026-10-13]]

## [2026-11-02] ingest — 헤르더 편대 구축과 미모·코코 복구

헤르더 앱 창에 에이전트 7마리를 올림. 핵심 규칙: `hc run --bg --name X --parent t1`처럼 **`--parent t1`을 붙여야** 앱 사이드바에 뜬다(앱은 자기 공간 안에서 시작한 터미널만 나열). 붙이지 않으면 CLI에는 보이나 앱에는 안 보인다.

**mimocode 함정(중요)**: npm의 `mimocode` 패키지는 샤오미 것이 아니라 `github.com/eurocybersecurite/mimocode`라는 남의 프로젝트다. 버전이 0.36.4로 표기되면서 로컬 런타임(llama-cpp·lmstudio·mlx·ollama)만 지원해 외부 API를 붙일 수 없다. 샤오미 정품은 `curl -fsSL https://mimo.xiaomi.com/install | bash`로 설치하는 별개 바이너리 `mimo` 0.1.9이며, `mimo providers`/`mimo models`로 OpenCode Go 모델을 그대로 인식한다. 두 달 동안 "미모"라 부르던 것이 실은 남의 프로그램이었다.

**코코 복구**: Claude Code가 첫 실행에서 "이 API 키 쓸래?" 물을 때 No를 누르면 `~/.claude.json`의 `customApiKeyResponses.rejected`에 키 뒷자리가 남아 계속 `Not logged in`이 된다. 승인 목록으로 옮기면 즉시 붙는다. 모델은 `muse-spark-1.3-contributor`.

**각 프레임워크 자체 검색 유무(실측)**: Claude Code는 `WebSearch`+`WebFetch` 내장(바이너리 언급 100/138회), Cline은 `web_search` 내장(166회), OpenCode는 `webfetch`만 있어 URL을 아는 경우만 가능하고 검색은 없다(지호에게 직접 물어 확인). 검색이 없는 곳에는 전 에이전트 공용 `~/.local/bin/free-search`(DDG AI Search → 로컬 추출 → Insane Search → browser_exec 폴백, 키 불필요)를 지침에 넣어야 실제로 쓴다.

검색 도구 배치: 해나만 brave-free + ddgs 추출 + Tavily 키(58자) 보유. 나머지는 프리서치가 유일한 무료 경로.

폐기: 웹사이트 클론 테스트(JCodesMore 템플릿, semiseron.kr 복제)는 확인 목적을 달성해 676MB 전체 삭제. 포트 3100 종료.

## [2026-11-02] ingest — Craft 앱들이 에이전트 조종을 지원함

storytold의 Craft 앱 8종을 확인한 결과 **전부 로컬 제어 서버를 내장**하고 있었다. WordCraft·PdfCraft·VectorCraft·PhotoCraft·FilmCraft·DeckCraft는 `--control PORT`, DesignCraft·EffectCraft는 문서상 지원. 즉 어도비·MS 대체 앱들을 에이전트가 직접 조종할 수 있다.

**DesignCraft 실측(핵심)**: InDesign 오픈소스 클론, Knuth-Plass 조판 엔진, `engine.commands`가 **709개** 명령을 반환. A4 3페이지 문서를 소켓 JSON lines로 조판해 인쇄용 PDF까지 뽑았다. 이전에 이북을 HTML로 페이지 나눠 만들다 제목이 잘리고 다음 장에 붙던 문제는 조판 엔진 부재가 원인이었고, 이 도구로 해결된다. IDML 양방향이라 InDesign과도 주고받는다.

**한글 폰트 함정**: 기본 폰트가 `Source Serif 4` 하나뿐이라 한글이 두부(□)로 깨진다. 시스템 폰트는 `font.reload`로 940개 인식되지만 문서에 지정되지 않은 상태. `font.replace {family:"Source Serif 4", toFamily:"Apple SD Gothic Neo", redefineStyles:true}` 후 PDF를 다시 뽑아야 반영된다.

**text.insert 함정**: `story` 파라미터를 받지 않는다(`text`, `raw`만). 프레임 생성 시 `text`로 한 번에 넣는 게 확실하다.

**document.inspect 함정**: 프레임·스토리는 생성됐는데 pages·items가 0으로 나오는 경우가 있다. PDF는 정상 출력되므로 이 값만 보고 실패로 판단하면 안 되고 PDF를 이미지로 뽑아 눈으로 확인해야 한다.

**중복 정리**: ieumoffice(42도구)·WordCraft·officecli가 워드/표/발표에서 겹친다. 일상 처리는 ieumoffice, 인쇄급 조판은 WordCraft, 페이지 조판은 DesignCraft, HWPX는 rhwp로 나눈다.

산출물: 서재 `책조판-designcraft.md`, `무기목록.md`(13분류), `video-tools/` 2건.

## 2026-11-05 — 모닝샘 C안 (9월에 멈춘 화면 되살리기)

**마스터님 지적**: 제53호까지 올라갔는데 카드·키워드·쉽게읽기가 전부 9월 것이다. 전수조사.

**원인**: `today-briefing.json`에는 제목·본문·시사점만 있었고, 카드·키워드·쉽게읽기는 `briefing.html`에 직접 박혀 2026-09-22 이후 미수정. 생성기는 매일 돌았지만 그릇이 4건짜리뿐. `ticker`는 매일 생성되고 버려지고 있었다.

**C안**: 1면·레일은 오늘 뉴스, 카드 3개는 최근 7일 흐름(아카이브 176건 재활용), 키워드는 AI가 후보 8개 중 4개 선택, 쉽게읽기 4세트 매일 갱신, ticker 화면에 살림.

**함정 3개**: ① `srcrow` innerHTML 교체가 쉽게읽기 버튼을 지운다(keepBtn으로 보존) ② 키워드를 4개 미만으로 넘기면 낡은 값이 남는다(단계적 기준 완화로 반드시 n개) ③ LLM이 주는 루트 도메인 링크는 기사 링크가 아니다(`#archive` 대체).

**검증** 49 PASS / 0 FAIL — 배포본과 로컬본 바이트 일치까지 확인.

산출물: `wiki/morningsam-c-plan.md`

## [2026-11-06] query — 도구 대장 신설: installed-tools · scrapling

Scrapling이 이미 설치돼 있었는데도 "우리 원래 깔려 있지 않아?" 질문을 받고서야 확인했다. 원인은 세 가지였다.

1. 설치 위치가 `~/.hermes/hermes-agent/venv/bin/` 안쪽이라 PATH에 없었다.
2. index.md에 `[[scrapling-mcp-guide]]`가 등재돼 있었지만 **해당 파일이 없었다**(죽은 링크).
3. 도구의 "존재"를 적는 페이지가 없었다.

조치:
- `~/.local/bin/scrapling` 심볼릭 링크로 PATH 노출
- `wiki/installed-tools.md` 신설 — 문제→도구 표 + 실측 경로 + "없다 답하기 전 디스크 확인" 철칙
- `wiki/scrapling.md` 신설 — TLS 위장 원리, 3종 수집기, 404/차단 혼동 함정
- index.md 죽은 링크 `scrapling-mcp-guide` → `scrapling` 교체
- 실측: docs.midjourney.com(Cloudflare) 헤드리스 크롬 차단 / Scrapling status 200 · 0.6초

## [2026-11-06] query — OpenCode Go 구독 API 함정 3종 기록

Muse Spark 1.3을 "크레딧 없어 못 쓴다"고 잘못 보고했다. 마스터님이 정정했고 원인을 규명했다.

- 엔드포인트: `/zen/v1`(종량제)이 아니라 **`/zen/go/v1`(구독)**
- 모델명: `muse-spark-1.3`이 아니라 **`muse-spark-1.3-contributor`**
- 헤더: **`x-opencode-session`** 필수 (임의 문자열 통과)
- 과금: 응답 `opencode.billing_source = go`, `cost: 0` → **추가 결제 없음**
- 추론 모델이라 `max_tokens` 2,000 미만이면 답이 빈다. 4,000~6,000 필요
- 파이썬 urllib은 403, curl은 통과

`installed-tools.md`에 표로 기록.
## [2026-11-09] note — semiseron.kr 파비콘 추가

- 증상: 브라우저 탭에 아이콘이 없음. `/favicon.ico` 404, head에 icon 링크 0개
- 조치: `symbol_light.png`에서 A만 잘라 잉크 바탕 타일 생성 → ico·32·48·192·512·apple-touch
- head에 링크 6줄 + `site.webmanifest` 추가
- 검증: 라이브 전부 200 (ico 450B, 32 1,085B, 192 7,259B)
- 기억할 것: **로고는 로고 전체를 쓴다.** A만 잘라 쓰면 마스터님이 바로 지적하신다 (같은 날 재작업, `e9dcbf9`)

## [2026-11-12] rule — 조직 명칭 3종 구분

- 마스터 지시: 새미새론 / 새미새론AI교육원 / 새미새론AI교육원 협동조합은 **각각 고유 명칭**이다
- 조치: `wiki/organization-names.md` 신설, index 등재
- 규칙: 브랜드=새미새론 · 교육 주체=새미새론AI교육원(붙여쓰기) · 법인=새미새론AI교육원 협동조합(협동조합 앞 띄어쓰기)
- 금지: 세미새론·세미세론·새미세론·새미새론AI교육원협동조합·KACEC
- 계기: 내가 대화에서 '세미새론'으로 잘못 적어 마스터님이 지적
