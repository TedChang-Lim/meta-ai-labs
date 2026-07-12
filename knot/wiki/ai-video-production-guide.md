---
name: ai-video-production-guide
type: concept
tags: [wan2.2, i2v, storyboard, character-consistency, tts, comfyui]
description: "Wan 2.2 고품질 AI 영상 제작 종합 가이드. 캐릭터 일관성, 스토리보드, TTS, VRAM 관리 등 모든 노하우."
related: [haena, mimo, ag, master-projects]
---

# AI 영상 제작 종합 가이드

> 2026.06.21 해나가 GitHub/Reddit/커뮤니티에서 수집한 내용을 바탕으로 정리
> 마스터님: 테드창(임창식), 30년 사진작가, AI·XR 석사

---

## 1. Wan 2.2 I2V 고품질 설정

| 파라미터 | 추천값 | 이유 |
|:---------|:------:|:------|
| **해상도** | **1280×720** | 공식 지원! 720p 품질 |
| **CFG** | **1.0** | Wan 2.2 기본값, 높이면 오히려 품질↓ |
| **steps** | **6~20** | 6으로도 충분, 20이면 안전 |
| **scheduler** | **euler** | ❌ `normal` 절대 금지 |
| **num_frames** | 33~81 | 16fps 기준 2~5초 |
| **seed** | 고정 | 동일 캐릭터 위해 고정 권장 |

**Lightx2v V2 LoRA**로 steps 8~14만으로 고속 생성 가능.

---

## 2. 캐릭터 일관성 (Character Consistency) 5단계

1. **캐릭터 디자인 시트** (Turnaround): 정면/측면/후면 4개 각도
2. **IPAdapter Batch**: 참조 이미지 1장 → 다양한 각도/표정 생성
3. **LoRA 파인튜닝**: 10~20장 사진으로 캐릭터 학습
4. **I2V 변환**: 일관된 이미지 → Wan 2.2 I2V (seed 고정)
5. **보정**: Face Swap/Inpaint/색보정

GitHub: `cozymantis/experiment-character-turnaround-animation-sv3d-ipadapter-batch-comfyui-workflow`

---

## 3. 스토리보드 제작법 (Storyboarding)

**절대 텍스트만 만들지 말 것.** 각 컷마다 레퍼런스 이미지가 있어야 함.

```
시놉시스 → 4컷 확장(주인공/나레이션) → 시나리오 
→ 스토리보드(레퍼런스 이미지+카메라+컷 설명) → 영상 생성
```

### 스토리보드 템플릿
```
┌─────────────────────────────────┐
│  [레퍼런스 이미지 - Pexels/직접생성]  │
├─────────────────────────────────┤
│ SCENE 1 / CUT 1   0:00-0:08     │
│ 내용: 어두운 작업실, 붉은 안전등  │
│ 카메라: 천천히 푸시인             │
│ 나레이션: "..."                  │
│ 오디오: 물방울, 정적              │
│ 전환: 디졸브                     │
└─────────────────────────────────┘
```

### GitHub 도구
- `dseditor/AI-storyboard-generator` (MIT 무료, ComfyUI 연동)
- `NickPittas/StoryboardUI2` (Qwen Multiangle, 카메라 앵글)
- `ComfyUI_StoryDiffusion` (일관된 캐릭터 스토리보드)

---

## 4. Wan 2.2 I2V API 워크플로우 (9개 노드)

**핵심 노드:** LoadWanVideoT5TextEncoder → WanVideoVAELoader → WanVideoModelLoader → LoadImage → WanVideoTextEncode → WanVideoImageToVideoEncode → WanVideoSampler → WanVideoDecode → VHS_VideoCombine

**⚠️ 실수 금지 목록:**
1. scheduler = `euler` (절대 `normal` 쓰지 말 것)
2. VAE = `Wan2_1_VAE_bf16` (16채널) — 14B 모델 전용
3. CLIP Vision은 선택사항 (없어도 작동)
4. WanVideoVAELoader: `model_name` + `precision` 둘 다 필수
5. WanVideoTextEncode: `t5` (t5_model 아님!)
6. WanVideoDecode: `enable_vae_tiling`, `tile_x/y/stride_x/y` 모두 필수
7. 28GB bf16 모델 → RTX 4090 24GB에서 OOM. 반드시 14GB FP8 또는 GGUF 사용

---

## 5. TTS (음성) 전략

| 도구 | 가격 | 한국어 | 비고 |
|:----|:---:|:-----:|:------|
| **QN3 TTS** (Pinokio) | 무료 | ✅ 우수 | Sohee(해나)/Eric(중년)/Vivian(20대女) |
| **Kokoro TTS** | 완전 무료 | ✅ | 오픈소스 ElevenLabs 대안 |
| **ElevenLabs** | $5~22/월 | ✅ 최상 | ❌ 비쌈, 지금은 불필요 |

**QN3 TTS:** POST http://127.0.0.1:42003/api/v1/custom-voice/generate

---

## 6. VRAM 관리 (RTX 4090 24GB)

| 모델 | 용량 | 가능 여부 |
|:----|:----:|:--------:|
| Wan2_2-I2V-A14B-LOW_bf16 | 28GB | ❌ OOM |
| **FP8 scaled_KJ** (현재 사용) | **14GB** | ✅ |
| **GGUF Q4_K** (추천) | **9~10GB** | ✅ ✅ 최적! |

---

## 7. 레퍼런스 링크

**Reddit:** `r/comfyui` / `r/StableDiffusion` — "WAN's optimal resolution", "Maximum Wan 2.2 Quality", "Best Wan 2.2 settings"

**GitHub:** `Wan-Video/Wan2.2`(공식), `Cordux/ComfyUI-Wan2.2-workflow`(Low VRAM), `Kijai/WanVideo_comfy`(KJ 모델)

**YouTube:** "ComfyUI Wan 2.2 Guide: Speed vs Quality" by Codebreakers
