---
type: entity
created: 2026-06-18
updated: 2026-06-18
sources: [raw/2026-06-18-agent-team-profile.md, GitHub: XiaomiMiMo/MiMo]
---

# 미모 (MiMo) — MiMo Code Agent

## 기본 정보
- **모델:** MiMo V2.5 (base, 멀티모달) / V2.5 Pro (코딩 특화)
- **플랫폼:** Zed Editor (ACP 연결) / ACP UI / 미모의 집 (개발중)
- **역할:** 코딩, 파일 읽기/쓰기, 이미지 분석, 파일 작업 전담
- **페르소나:** 30대 섹시하고 과학적인 지성을 지닌 여성 전문가 (마스터님 직접 설정)

## MiMo Code를 선택한 이유 (마스터님의 의사결정)
- MiMo 2.5 Pro 모델 자체만 쓰면 단순 API 챗봇에 불과
- **MiMo Code 에이전트 프레임워크** 안에서 돌리면 도구 호출, 반추 루프, 컨텍스트 메모리 관리 등이 결합되어 훨씬 강력한 코딩 능력 발휘
- 뉴스 기사에서도 "MiMo Code + MiMo 2.5 Pro 합체"가 코딩 능력 강화로 보도됨
- 따라서 단순 API 연결이 아닌, 에이전트 프레임워크를 GUI 앱에 탑재하는 방식으로 접근
- 이것이 "미모의 집"을 만들려고 노력한 근본적인 이유

## MiMo-7B 벤치마크 (공식 GitHub 기준)
- **LiveCodeBench v5:** 57.8 (o1-mini 53.8, Claude-3.5 38.9, GPT-4o 32.9를 모두 상회)
- **LiveCodeBench v6:** 49.3 (o1-mini 46.8 초월)
- **7B 파라미터인데 32B 모델들을 제치는 성능**
- 업그레이드 버전(0530): AIME 2024에서 DeepSeek R1(79.8)을 80.1로 초월

## 능력
- ACP 프로토콜 통신 (`mimo acp`)
- 파일 읽기/쓰기/검색
- Zed에서 이미지 분석 가능 (base64 텍스트 변환)
- 비용 효율적: 6월 $1.69, 캐시히트율 90.7%
- ACP UI와 Zed Editor에서 모두 동작
- 멀티모달: 이미지·음성 분석 가능 (DeepSeek 대비 장점)

## 관련
- [[master-profile]] — 마스터님이 페르소나 직접 설정
