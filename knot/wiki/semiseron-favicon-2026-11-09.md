---
type: note
created: 2026-11-09
updated: 2026-11-09
sources: [semiseron.kr 배포 저장소 TedChang-Lim/meta-ai-labs]
aliases: [파비콘, favicon]
---

# semiseron.kr 파비콘 (2026-11-09)

브라우저 탭에 아무 표시도 없던 상태를 고쳐, 새미새론 심볼(A)을 탭 아이콘으로 넣었다.

## 확인한 결함

- `https://semiseron.kr/favicon.ico` → **404** (9,379B 오류 페이지)
- `index.html` 에 `rel="icon"` 링크 **0개**
- 그래서 탭에 브라우저 기본 아이콘만 보였다.

## 만든 것

| 파일 | 크기 | 용도 |
|---|---|---|
| `favicon.ico` | 16·32·48 | 브라우저 기본 |
| `favicon-32x32.png` · `favicon-48x48.png` | 각 크기 | 탭·북마크 |
| `favicon-192x192.png` · `favicon-512x512.png` | 각 크기 | 안드로이드·PWA |
| `apple-touch-icon.png` | 180 | iOS 홈 화면 |
| `site.webmanifest` | — | 이름·테마색(#080908) |

원본은 `assets/logo/symbol_light.png` **전체**(A + 세로 '새·미·새·론' + 별 3개)를 쓴다.
처음에 A만 잘라 넣었다가 마스터님이 "로고를 파비콘으로 만들어야지 A자 하면 뭐냐"고 지적해
전체로 교체했다(커밋 `e9dcbf9`). 16px에서는 세로 글자가 점처럼 뭉개지지만, 로고를 알아볼 수 있게
A의 실루엣이 남으므로 이대로 쓴다.

## head에 넣은 것

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192x192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#080908">
```

## 검증

라이브 응답 전부 200.

```
/favicon.ico            200  image/vnd.microsoft.icon  450B
/favicon-32x32.png      200  image/png                1,085B
/favicon-192x192.png    200  image/png                7,259B
/apple-touch-icon.png   200  image/png                6,050B
/site.webmanifest       200  application/manifest+json
```

## 다음에 할 때

- 브라우저는 파비콘을 오래 캐시한다. 안 바뀌면 **탭을 닫고 새로 열거나** `?v=2` 로 확인.
- 로고가 바뀌면 `assets/logo/symbol_light.png` 에서 `A` 영역(x 120~695)만 다시 잘라 같은 절차로 생성.
- 아이콘 링크가 이미 있으면 스크립트가 중단되게 해 두었다(중복 삽입 방지).
