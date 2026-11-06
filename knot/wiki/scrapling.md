---
type: entity
created: 2026-11-06
updated: 2026-11-06
sources: []
aliases: [스크래플링, Scrapling, 스크래핑]
---

# Scrapling — 막힌 사이트를 뚫는 수집 도구

## 한 줄

**봇 차단(403·429·Cloudflare)에 막혔을 때 가장 먼저 꺼내는 도구.** 파이썬 라이브러리이자 CLI.

## 어디에 있나 (실측 2026-11-06)

```
껍데기   ~/.local/bin/scrapling
본체     ~/.hermes/hermes-agent/venv/bin/scrapling
버전     0.5
도우미   patchright 1.64.4 · playwright 1.64.1 · curl_cffi 0.17.0
```

**주의:** 원래 Hermes 전용 가상환경 안에만 있어서 PATH에 없었다. 2026-11-06에 `~/.local/bin`으로 심볼릭 링크를 걸어 다른 에이전트도 쓸 수 있게 했다.

## 왜 뚫리는가

일반 헤드리스 크롬은 TLS 지문·헤더·JS 흔적으로 봇 판정을 받는다. Scrapling은 **curl_cffi로 실제 브라우저의 TLS 지문을 흉내**내므로, 같은 페이지를 크롬으로 열면 막히고 Scrapling으로 열면 통과한다.

## 실측 사례 (2026-11-06)

```
대상   docs.midjourney.com (Cloudflare 보호)
헤드리스 크롬   "보안 확인 수행 중" 차단 화면
Scrapling       status 200 · 0.6초 · 본문 정상 수신
```

이때 공식 요금표를 그대로 받아왔다. 같은 페이지를 브라우저 도구로 열면 Cloudflare 챌린지에 걸린다.

## 쓰는 법

```bash
scrapling --help
```

파이썬에서:

```python
from scrapling.fetchers import Fetcher
p = Fetcher.get("https://example.com/blocked", timeout=40)
text = p.get_all_text()
```

세 가지 수집기:

| 수집기 | 방식 | 언제 |
|---|---|---|
| `Fetcher` | HTTP + TLS 위장 | **먼저 이걸 쓴다.** 가장 빠르고 대부분 통과 |
| `DynamicFetcher` | 실제 크로미움(patchright) | JS 렌더가 필요할 때 |
| `StealthyFetcher` | camoufox 위장 브라우저 | 위 둘이 다 막힐 때. **현재 camoufox 미설치** (`scrapling install`로 받아야 함) |

## 함정

- **404를 차단으로 오해하지 않는다.** 2026-11-06에 "Cloudflare에 막혔다"고 판단한 것이 실은 문서 번호가 바뀐 404였다. Scrapling은 상태 코드를 그대로 보여주므로 **먼저 status를 읽는다.**
- **camoufox는 아직 없다.** `StealthyFetcher`는 설치 전까지 실패한다. 먼저 `Fetcher`와 `DynamicFetcher`로 시도한다.
- **venv 안에만 있으면 다른 에이전트가 못 쓴다.** 새 환경에 깔 때도 반드시 `~/.local/bin`에 노출한다.

## 관련

- [[installed-tools]]
- [[insane-search-extract]]
