# PDF Masking Tool v1.5

PyQt6와 PyMuPDF를 기반으로 한 전문적인 PDF 문서 마스킹 도구입니다.

## ✨ 주요 기능

- 🖱️ **Ctrl + 드래그**로 마스킹 영역 선택 (실시간 미리보기)
- ⚪ **영구 제거**: PyMuPDF Redaction으로 원본 데이터 완전 삭제
- 💾 **자동 백업**: 원본 PDF를 일자별 폴더에 백업
- 📂 **폴더 일괄 처리**: 여러 PDF 파일을 순차적으로 작업
- 🔄 **진행 상황 복구**: 작업 중단 후 이어서 재개 가능
- 📊 **작업 이력 관리**: JSON 로그 및 상세 로그 자동 기록
- � **암호화된 PDF 지원**: 암호로 보호된 PDF 파일 열기 지원
- �🔒 **라이선스 인증**: 시리얼 번호 기반 접근 제어

## 🚀 빠른 시작

### 설치
```bash
git clone https://github.com/yourusername/pdfmask.git
cd pdfmask
uv sync
```

### 실행
```bash
# 방법 1: 직접 실행
uv run python src/main.py

# 방법 2: 스크립트로 실행
uv run pdfmask
```

### 첫 실행 시
- 라이선스 인증 다이얼로그 표시
- 테스트 시리얼: `TEST-1234-5678-ABCD` 또는 `DEMO-0000-0000-0001`

## ⌨️ 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+Shift+O` | 폴더 열기 |
| `Ctrl+S` | 마스킹 저장 |
| `Ctrl+드래그` | 마스킹 영역 선택 |
| `Ctrl+휠` | 확대/축소 (50%~200%) |
| `←` / `→` | 이전/다음 페이지 |
| `Del` | 마스킹 삭제 |
| `더블클릭` | 메모 편집 |

## 📖 사용 방법

### 1. PDF 작업 시작
```
폴더 열기 (Ctrl+Shift+O)
  ↓
마스킹 영역 선택 (Ctrl+드래그)
  ↓
메모 추가 (더블클릭)
  ↓
저장 (Ctrl+S)
  ↓
다음 파일로 자동 이동
```

### 2. 마스킹 작업
1. **영역 선택**: `Ctrl` 키를 누른 상태에서 드래그
   - 드래그 중: 파란색 표시
   - 저장 후: 빨간색 표시
2. **메모 추가**: 왼쪽 리스트에서 "메모" 셀 더블클릭
3. **삭제**: 항목 선택 후 `Del` 키

### 3. 저장 프로세스 (자동화)
```
Ctrl+S 누름
  ↓
원본 백업 (backup/YYYYMMDD/)
  ↓
Redaction 적용 (흰색, 영구 제거)
  ↓
데이터 저장 (mask_data_YYYYMMDD.json)
  ↓
진행 상황 업데이트 (progress.json)
  ↓
로그 기록 (pdfmask_YYYYMMDD.log)
  ↓
다음 파일 이동 제안
```

## 📂 프로젝트 구조

```
pdfmask/
├── src/                       # 소스 코드
│   ├── main.py               # 애플리케이션 진입점 (50줄)
│   └── pdfmask/              # 메인 패키지 (모듈화)
│       ├── core/             # 데이터 모델 (MaskEntry)
│       ├── managers/         # 비즈니스 로직 (5개 Manager)
│       ├── ui/               # UI 컴포넌트 (4개 클래스)
│       └── utils/            # 유틸리티 (향후 확장)
│
├── docs/                      # 📚 개발자 문서
│   ├── SPECIFICATION.md      # 기능 명세서 (1500줄)
│   ├── ARCHITECTURE.md       # 아키텍처 문서 (800줄)
│   ├── PROJECT_SUMMARY.md    # 프로젝트 요약 (600줄)
│   ├── REFACTORING_SUMMARY.md # 리팩토링 요약 (500줄)
│   └── QUICK_START.md        # 빠른 시작 가이드 (400줄)
│
├── backup/                    # 원본 백업 (일자별, 자동 생성)
│   └── YYYYMMDD/*.pdf
├── masks_data/                # 마스킹 데이터 (일자별, 자동 생성)
│   └── mask_data_YYYYMMDD.json
├── logs/                      # 로그 파일 (일자별, 자동 생성)
│   └── pdfmask_YYYYMMDD.log
├── xls/                       # 엑셀 작업 내역 (일자별, 자동 생성)
│   └── 마스킹_작업내역_YYYYMMDD.xlsx
│
├── progress.json              # 진행 상황 (자동 생성/삭제)
├── .license                   # 라이선스 (인증 후 생성)
├── pyproject.toml             # 프로젝트 설정
├── README.md                  # 📖 사용자 가이드 (본 문서)
└── DEVLOG.md                  # 개발 로그
```

## 🎨 UI 구성

```
┌────────────────────────────────────────────┐
│ [PDF 열기] [폴더 열기]  메뉴바              │
├──────────┬─────────────────┬───────────────┤
│ 마스킹   │  PDF 뷰어       │  파일 목록    │
│ 리스트   │  (회색 배경)     │               │
│          │  ┌───────────┐  │  ✓ file1.pdf  │
│ 페이지|메모│  │ PDF 내용 │  │    file2.pdf  │
│ 1 | 주민번호│  │ (흰색)   │  │    file3.pdf  │
│ 1 | 전화번호│  └───────────┘  │               │
├──────────┴─────────────────┴───────────────┤
│ 페이지: 1/10 | 확대: 100% | Ctrl+드래그...  │
└────────────────────────────────────────────┘
```

## ⚠️ 주의사항

1. **영구 마스킹**: Redaction은 복구 불가능 (백업 활성화 권장)
2. **파일 잠금**: PDF를 다른 프로그램에서 닫고 저장
3. **백업 설정**: `설정 > PDF 백업 활성화` (기본: 활성화)

## 🛠️ 기술 스택

| 구분 | 기술 |
|------|------|
| GUI | PyQt6 6.5.0+ |
| PDF | PyMuPDF (fitz) 1.26.6+ |
| 언어 | Python 3.12+ |
| 패키지 관리 | uv |

## 🐛 문제 해결

| 문제 | 해결 |
|------|------|
| "Permission denied" | PDF를 다른 프로그램에서 닫기 |
| 확대/축소 안됨 | `Ctrl` 키 누른 상태에서 휠 |
| 마스킹 드래그 안됨 | `Ctrl` 키 누른 상태에서 드래그 |
| 독 위젯 재결합 안됨 | 창 최대화 해제 후 재시도 |
| 암호화된 PDF 열기 | 암호 입력 다이얼로그에서 올바른 암호 입력 |

## 📊 주요 클래스

```python
# 데이터 구조
@dataclass
class MaskEntry:
    page_index: int      # 0-based (내부), 1-based (UI)
    rect: fitz.Rect      # PDF 좌표계
    note: str = ""       # 사용자 메모

# 관리자 클래스
PdfDocumentManager    # PDF 로드, 렌더링, Redaction
LicenseManager        # 라이선스 인증
MaskDataManager       # 마스킹 데이터 JSON 관리
ProgressManager       # 진행 상황 추적
LogManager            # 로그 기록
```

## 🔧 시스템 요구사항

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.12+
- **메모리**: 4GB (큰 PDF: 8GB 권장)
- **디스크**: 백업 및 로그 저장 공간

## 📝 버전 히스토리

### v1.5.1 (2025-12-16)
- ✨ **암호화된 PDF 지원**: 암호로 보호된 PDF 파일 열기 기능 추가
  - `PasswordInputDialog` 다이얼로그로 암호 입력 처리
  - 잘못된 암호 입력 시 재시도 가능
- 🐛 **확대/축소 기능 수정**: PDF 화면 위에서 `Ctrl + 휠` 동작하지 않는 버그 수정
  - `QScrollArea.setWidget()` 사용 시 부모 위젯 참조 문제 해결
  - `parent()` 대신 `window()`를 사용하여 MainWindow 탐색으로 변경

### v1.5.0 (2025-11-19)
- ✨ **프로젝트 모듈화**: 코드를 기능별 모듈로 분리 (core, managers, ui, utils)
- 📚 **문서화 완료**: 기능명세서, 아키텍처 문서, 프로젝트 요약 작성
- 🔧 **유지보수성 향상**: 파일당 평균 150줄로 관리 용이
- 📂 **구조 개선**: 명확한 책임 분담 및 확장성 확보

### v1.5 (2025-11-18)
- ✨ PDF 자동 백업 / 라이선스 인증
- ✨ 마스킹 데이터 JSON / 진행 상황 추적
- ✨ 상세 로그 기록 (좌표 포함)

### v1.0 (2025-11-17)
- 🎉 첫 번째 정식 릴리스

## 📖 추가 정보

### 사용자용 문서
- **빠른 시작**: [docs/QUICK_START.md](docs/QUICK_START.md) - 5분 안에 시작하기
- **개발 로그**: [DEVLOG.md](DEVLOG.md) - 개발 히스토리

### 개발자용 문서
- **기능 명세서**: [docs/SPECIFICATION.md](docs/SPECIFICATION.md) - 클래스, 메서드 상세 설명
- **아키텍처**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - 설계 원칙, 확장 가이드
- **프로젝트 요약**: [docs/PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) - 빠른 참조, 온보딩
- **리팩토링 요약**: [docs/REFACTORING_SUMMARY.md](docs/REFACTORING_SUMMARY.md) - v1.5.0 변경사항

### 기타
- **라이선스**: 자유롭게 사용 가능
- **기여**: 버그 리포트, 기능 제안 환영
- **GitHub**: Issues 및 Pull Requests 환영

---

**PDF Masking Tool** - 빠르고 안전한 PDF 개인정보 마스킹 솔루션
