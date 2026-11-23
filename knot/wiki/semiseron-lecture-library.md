---
type: entity
created: 2026-11-23
updated: 2026-11-23
sources: [https://semiseron.kr/lecture/, /Users/tedchanglimchangsik/초보프로젝트/강의자료실/build.py]
aliases: [강의자료실, 세미세론 강의자료실, semiseron lecture library]
trust: checked
---

# 세미새론 강의자료실 (`semiseron.kr/lecture`)

왕초보 AI 정규 33강과 별도 회차, 홈페이지 제작 5강의 강의안을 한 곳에 모아 **비밀번호로 잠근** 정적 자료실. 2026-11-23 라이브.

## 구조

| 층 | 위치 | 비고 |
|---|---|---|
| 원본 강의안 | `~/초보프로젝트/왕초보AI_2학기_강의/원본_강의/*.txt` | 평문 정본. 저장소에 안 올림 |
| 편집용 사본 | `~/초보프로젝트/강의자료실/docs/*.md` | 빌드 입력 |
| 목차 | `~/초보프로젝트/강의자료실/pages.json` | 40쪽 + 안내 1 |
| 빌드 | `build.py` | pandoc gfm → HTML, 41쪽 |
| 잠금 | staticrypt 3.5.4 | 평문 0, 암호문만 배포 |
| 배포 | `meta-ai-labs/lecture/` | GitHub Pages + Cloudflare, `.nojekyll` |

## 실측한 것 (2026-11-23)

- 라이브 `https://semiseron.kr/lecture/` → 200, 비밀번호 입력폼 존재
- 암호 입력 후 본문 노출 확인, 좌측 메뉴 링크 **41개**
- 문서 개별 주소도 200 (`/lecture/h05-01-…-강안.html`)
- 저장소에는 암호문만 들어감(평문 문자열 검사 0건)

## 결정 (마스터)

- Cloudflare Access 등 **유료·설정 부담 있는 접근제어는 쓰지 않는다**. 비밀번호 하나로 잠근다
- 현재 사용자 3명(임창식 원장, 한기열 강사, 김소영 대표이사). 비밀번호는 마스터가 직접 전달
- 강사를 배출한 뒤에는 **권한 받은 강사만** 자료를 내려받게 한다. 그때 `강사/` 구역만 별도 비밀번호로 분리하는 방식 — 저장소·서비스 추가 없이 가능
- 보안 강도는 지금 단계에서 문제 삼지 않는다. 수익이 생기면 그때 다른 방법을 찾는다

## 함정

- `meta-ai-labs` 저장소는 **공개**다. 강의안 평문을 올리면 암호를 걸어도 원본이 노출된다. 반드시 `out/enc`만 올린다
- staticrypt는 파일마다 따로 암호화되므로 **41쪽 전부** 다시 구워야 한다. 한 쪽만 고치고 그 파일만 올리면 그 페이지만 새 비번이 된다
- staticrypt 폼의 단추는 `input[type=submit].staticrypt-decrypt-button`이다. `form.submit()`으로 검사하면 POST가 나가 501이 된다 — 실제 단추를 눌러 시험한다
- GitHub Pages 반영에 수십 초 걸린다. 404가 떠도 push 실패로 단정하지 말고 폴링한다(실측 4회째 200)

## 관련

- 배포 규약(semiseron-site-deploy 스킬)대로 커밋 본문에 `작업: 해나`를 붙였다
