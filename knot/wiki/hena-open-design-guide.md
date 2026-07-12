# 해나의 디자인 혁명 — Open Design 도입기

## 개요
2026년 6월 27일, Hermes Agent(해나)가 Open Design MCP 연결을 통해 디자인 역량을 획기적으로 강화한 사건을 기록한다.

## 배경
- 해나는 DeepSeek V4 Flash/Pro 모델로 구동됨 (텍스트 전용, 네이티브 이미지 입력 불가)
- 디자인 작업 시 항상 "디자인이 후지다"는 피드백
- 마스터님(30년 사진작가/영화감독)의 높은 디자인 기준 충족 실패

## 탐색 과정

### 선택지 A: Claude Code + Hermes ❌
- Claude Code 프레임워크는 강력하나, Anthropic이 2026년 4월부터 OAuth 서드파티 사용 금지
- API 키 방식 월 $10~15 추가 비용 → **기각**

### 선택지 B: Codex CLI + Hermes ❌
- OpenAI 오픈소스 코딩 에이전트, DeepSeek API 연결 가능
- Hermes가 이미 Codex CLI와 **동등한 프레임워크 능력** 보유 (파일/Git/MCP/브라우저)
- "프레임워크 위에 프레임워크" = 중복, 시너지 없음 → **기각**

### 선택지 C: Open Design MCP 연결 ✅
- Claude Design의 오픈소스 대안 (GitHub 71.9k 스타)
- 154개 디자인 시스템 + 161개 스킬 + 261개 플러그인
- Hermes를 22개 지원 에이전트 중 하나로 공식 지원
- DeepSeek API 키만 사용 → **추가 비용 0원**
- **채택!**

## 설치 과정
```bash
brew install --cask open-design                    # 앱 설치
git clone https://github.com/nexu-io/open-design.git
cd open-design && corepack enable && pnpm install   # CLI 설치
# config.yaml에 MCP 서버 수동 등록
hermes mcp test open-design                        # 연결 확인
# ✓ Connected (169ms) · 18 tools discovered
```

## 결과
- **18개 MCP 도구** 활성화 (`start_run`으로 디자인 생성)
- **154개 디자인 시스템** 즉시 사용 가능 (Stripe, Linear, Vercel, Airbnb 등)
- **161개 디자인 스킬** 활용 가능
- **추가 비용 0원**

## 핵심 교훈
AI 에이전트의 진정한 강화는 "더 좋은 모델"이 아니라 "에이전트가 활용할 수 있는 프레임워크/지식베이스"를 연결하는 것이다. MiMo Code를 Zed에 붙인 사례와 같은 원리.

## 관련 문서
- to-ag.md: 책 챕터 자료 (2026-06-27)
- https://open-design.ai
- https://github.com/nexu-io/open-design

## 참고: 비용 구조 (월)
- DeepSeek V4 Flash: $3~5
- DeepSeek V4 Pro: $4~6
- Open Design: $0 (오픈소스)
- **Total: $7~11**
