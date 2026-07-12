# ☀️ 헤나 위스퍼 (Hena Whisper) - v1.0 / v1.1
> **Groq Whisper API를 활용한 macOS Push-to-Talk 음성 받아쓰기 유틸리티**

헤나 위스퍼(Hena Whisper)는 시스템 자원(VRAM)을 소모하지 않고, 오른쪽 커맨드(Right Command) 키 하나만으로 빠르게 고성능 음성 인식을 지원하는 macOS 백그라운드 유틸리티입니다. 이 도구는 MacWhisper 등 로컬 Whisper 모델의 높은 GPU 메모리(VRAM) 점유율 문제를 완벽하게 해결하고, 마스터님의 M1/M2/M3 Mac에 실행 중인 다른 LLM(예: Qwen 35B)과 무리 없이 병행해서 사용할 수 있도록 제작되었습니다.

---

## 🚀 주요 특징 (Key Features)

1. **VRAM 0% 점유 (클라우드 오프로딩)**
   * 받아쓰기 연산을 로컬 GPU가 아닌 **Groq Whisper Cloud API (`whisper-large-v3`)**로 전송하여 약 100ms 내외의 초고속 속도로 실시간 텍스트 인식을 처리합니다.

2. **메뉴바 기반 상태 표시기 (🎙️, 🔴, 📡, ✅)**
   * 화면 최상단 메뉴바 아이콘의 모양을 통해 실시간으로 작동 상태를 알려줍니다.
     * `🎙️` : 대기 중 (Idle)
     * `🔴` : 녹음 중 (Recording)
     * `📡` : Groq API 전송 및 받아쓰기 중 (Transcribing)
     * `✅` : 입력 완료 및 텍스트 자동 붙여넣기 성공 (Pasted)
     * `⚠️` : macOS 손쉬운 사용(Accessibility) 권한 없음
     * `❌` : 네트워크 에러 또는 API 에러 발생

3. **손쉬운 사용 권한 실시간 감지 (TCC 바이패스)**
   * macOS 14+ 보안 버그로 인해 앱 빌드 시 권한 스위치가 풀리는 현상을 방지하기 위해 백그라운드 타이머가 작동합니다.
   * 권한이 없으면 메뉴바에 `⚠️` 아이콘이 뜨며, 시스템 설정에서 스위치를 켜는 즉시 앱 재시작 없이 실시간으로 `🎙️` 아이콘으로 전환되어 키 입력 감지를 시작합니다.

4. **클립보드 방식의 완벽한 한글 타이핑**
   * 일반적인 자판 입력 시뮬레이션에서 발생하는 한글 자모 분리 현상이나 오타를 원천 차단하기 위해 **NSPasteboard** 복사 후 **Cmd+V 키 시뮬레이션** 방식을 사용합니다. 띄어쓰기, 문장 부호, 영어 및 한글 혼용이 완벽하게 지원됩니다.

---

## 🛠️ 설치 및 컴파일 방법 (Compilation & Build)

HenaWhisper는 서명 및 디렉토리 구조를 포함한 macOS App Bundle 구조로 컴파일됩니다.

### 1. 디렉토리 구조
```text
HenaWhisper/
├── main.swift             # Swift 메인 소스 코드
├── Info.plist             # macOS App Bundle 정보 설정 파일
└── HenaWhisper.app/       # 컴파일된 최종 macOS 실행 앱
    └── Contents/
        ├── Info.plist
        └── MacOS/
            └── HenaWhisper  # 빌드된 바이너리 실행 파일
```

### 2. 빌드 명령어
터미널에서 `HenaWhisper` 폴더 경로로 이동 후 아래 명령어를 실행하여 빌드 및 코드 서명(codesign)을 진행할 수 있습니다.
```bash
# 1. 앱 번들 내 실행 경로 디렉토리 생성
mkdir -p HenaWhisper.app/Contents/MacOS HenaWhisper.app/Contents/Resources

# 2. Info.plist 복사
cp Info.plist HenaWhisper.app/Contents/Info.plist

# 3. Swift 소스 코드 컴파일
swiftc -o HenaWhisper.app/Contents/MacOS/HenaWhisper main.swift

# 4. 임시 임의 코드 서명 (Gatekeeper 방지)
codesign --force --sign - HenaWhisper.app

# 5. 앱 실행
open HenaWhisper.app
```

---

## ⚙️ 설정 가이드 (Configuration Guide)

앱 최초 실행 시 홈 디렉토리에 **`~/.hena_whisper.json`** 설정 파일이 자동으로 생성됩니다. 텍스트 에디터로 열어 자유롭게 모델과 단축키를 변경할 수 있습니다.

* **설정 파일 경로:** `/Users/tedchanglimchangsik/.hena_whisper.json`

```json
{
  "api_key": "gsk_sku7jD2y...",
  "model": "whisper-large-v3",
  "language": "ko",
  "hotkey": "RightCommand"
}
```

### 설정 값 상세 설명
* `api_key` : 마스터님의 Groq API Key입니다.
* `model` : Groq에서 제공하는 Whisper 모델 ID입니다. (기본값: `whisper-large-v3`)
* `language` : 음성 인식의 우선 언어 코드입니다. (한국어 기본값: `ko`)
* `hotkey` : 푸시투토크 작동 키입니다. `RightCommand` (오른쪽 커맨드 키) 또는 `RightOption` (오른쪽 옵션 키)를 지정할 수 있습니다.

---

## 🐛 v1.1 패치 노트 — 클립보드 백업/복원 (2026.06.13)

### 버그
음성 입력 후 Cmd+V로 붙여넣기 하면 원래 복사해둔 텍스트가 사라지고 방금 말한 STT 텍스트가 붙는 문제.

### 해결
`pasteText()`에 **백업/복원 로직** 추가:
1. 붙여넣기 전에 기존 클립보드 텍스트를 변수에 저장
2. STT 텍스트 복사 → Cmd+V 시뮬레이션
3. 0.2초 후 백그라운드에서 기존 클립보드 자동 복원

---

## 🎭 에이전트 3인 디버깅 히스토리

* **마스터님**: 버그 발견, "Right Command 포기 불가" 최종 결정 및 시스템 권한 세팅
* **헤나**: 코어 코드 분석, 초기 빌드/배포 및 임의 코드 서명
* **에이지**: Groq Whisper 연동 및 붙여넣기 후 클립보드 복원 설계
