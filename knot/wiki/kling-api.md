---
type: entity
name: kling-api
title: Kling AI API
tags: [kling, api, video-generation]
---

## Kling AI API 정보

| 항목 | 내용 |
|:----|:------|
| **플랫폼** | [Kling AI](https://klingai.com) (Kuaishou) |
| **요금제** | Pro $37/월 (3,000크레딧) |
| **크레딧 잔액** | 3,069P (2026-06-15 기준) |
| **API 키 이름** | 해나AG잔 멋진영상만들기 |
| **API 키 저장 위치** | `~/.hermes/.env` → `KLING_API_KEY` |
| **API 문서** | [Kling API Docs](https://kling.ai/document-api/apiReference/model/imageToVideo) |
| **API 엔드포인트** | `https://api.klingai.com` |

## API 특징

- **비동기 방식**: 작업 제출(POST) → task ID → 완료 후 조회(GET)
- **영상 길이**: 5초 / 10초 (Standard), 최대 15초 (Pro)
- **모드**: Standard (워터마크 있음) / Professional (워터마크 없음)
- **크레딧**: Standard 5초=60P, 15초=180P, Custom Multi-Shot=540P

## 지원 기능

- [x] Text-to-Video (텍스트 → 영상)
- [x] Image-to-Video (이미지 → 영상, 얼굴 레퍼런스 유지)
- [x] Multi-Shot (여러 장면 연결)
- [x] Camera Motion (카메라 무빙 제어)
- [x] End Image (마지막 프레임 지정)

## 사용 예정 용도

- 1분 30초 오리지널 시네마틱 티저 트레일러
- 공모전 출품작
- 연출력 자랑용

## 관련 링크

- [Hermes config](../index.md) — API 호출 스크립트 정보
- [master-projects](../wiki/master-projects.md) — 영상 공모전 프로젝트
