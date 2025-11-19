# PDF Mask 기능 명세서

버전: 1.5.0  
작성일: 2025-11-19

---

## 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [디렉터리 구조](#디렉터리-구조)
3. [모듈 구조](#모듈-구조)
4. [클래스 및 메서드 명세](#클래스-및-메서드-명세)
5. [데이터 흐름](#데이터-흐름)
6. [실행 방법](#실행-방법)

---

## 프로젝트 개요

PDF Mask는 PDF 문서의 민감한 정보를 영구적으로 마스킹(Redaction)하는 PyQt6 기반 GUI 애플리케이션입니다.

### 주요 기능

- **마스킹 영역 선택**: Ctrl + 드래그로 실시간 미리보기
- **영구 제거**: PyMuPDF Redaction으로 원본 데이터 완전 삭제
- **자동 백업**: 원본 PDF를 일자별 폴더에 백업
- **폴더 일괄 처리**: 여러 PDF 파일을 순차적으로 작업
- **진행 상황 복구**: 작업 중단 후 이어서 재개 가능
- **작업 이력 관리**: JSON 로그 및 상세 로그 자동 기록
- **라이선스 인증**: 시리얼 번호 기반 접근 제어

---

## 디렉터리 구조

```
pdfmask/
├── src/
│   ├── main.py                    # 애플리케이션 진입점
│   └── pdfmask/                   # 메인 패키지
│       ├── __init__.py
│       ├── core/                  # 핵심 데이터 모델
│       │   ├── __init__.py
│       │   └── models.py          # MaskEntry 데이터 클래스
│       ├── managers/              # 관리자 클래스
│       │   ├── __init__.py
│       │   ├── license_manager.py # 라이선스 관리
│       │   ├── pdf_manager.py     # PDF 문서 관리
│       │   ├── mask_data_manager.py # 마스킹 데이터 관리
│       │   ├── progress_manager.py # 진행상황 관리
│       │   └── log_manager.py     # 로그 관리
│       ├── ui/                    # UI 컴포넌트
│       │   ├── __init__.py
│       │   ├── main_window.py     # 메인 윈도우
│       │   ├── pdf_view.py        # PDF 뷰어 위젯
│       │   └── dialogs.py         # 다이얼로그
│       └── utils/                 # 유틸리티
│           └── __init__.py
├── backup/                        # PDF 백업 폴더 (자동 생성)
│   └── YYYYMMDD/
├── masks_data/                    # 마스킹 데이터 (자동 생성)
│   └── mask_data_YYYYMMDD.json
├── logs/                          # 로그 파일 (자동 생성)
│   └── pdfmask_YYYYMMDD.log
├── .license                       # 라이선스 파일 (자동 생성)
├── progress.json                  # 진행상황 (자동 생성/삭제)
├── pyproject.toml                 # 프로젝트 설정
├── README.md                      # 사용자 가이드
└── SPECIFICATION.md               # 기능 명세서 (본 문서)
```

---

## 모듈 구조

### 1. Core Module (`src/pdfmask/core/`)

핵심 데이터 모델을 정의합니다.

#### `models.py`

- **MaskEntry**: 마스킹 정보를 저장하는 데이터 클래스

### 2. Managers Module (`src/pdfmask/managers/`)

각종 관리 기능을 담당하는 클래스들입니다.

#### 주요 클래스

- **LicenseManager**: 라이선스 인증 및 관리
- **PdfDocumentManager**: PDF 로드, 렌더링, 마스킹 적용
- **MaskDataManager**: 마스킹 데이터 JSON 저장/로드
- **ProgressManager**: 작업 진행상황 추적
- **LogManager**: 로그 기록

### 3. UI Module (`src/pdfmask/ui/`)

사용자 인터페이스 컴포넌트입니다.

#### 주요 클래스

- **MainWindow**: 메인 애플리케이션 윈도우
- **PdfPageView**: PDF 페이지 표시 및 마스킹 선택 위젯
- **ScrollablePdfView**: 스크롤 가능한 PDF 뷰 컨테이너
- **SerialInputDialog**: 라이선스 시리얼 번호 입력 다이얼로그

### 4. Utils Module (`src/pdfmask/utils/`)

공통 유틸리티 함수 (향후 확장 가능)

---

## 클래스 및 메서드 명세

### Core Module

#### `MaskEntry` (데이터 클래스)

```python
@dataclass
class MaskEntry:
    page_index: int      # 페이지 인덱스 (0-based)
    rect: fitz.Rect      # 마스킹 영역 좌표 (PDF 좌표계)
    note: str = ""       # 사용자 메모
```

**목적**: 마스킹 영역의 정보를 저장합니다.

---

### Managers Module

#### `LicenseManager`

라이선스 인증 및 관리를 담당합니다.

**속성**:
- `project_root`: 프로젝트 루트 경로
- `license_file`: 라이선스 파일 경로 (.license)

**메서드**:

```python
def __init__(self) -> None
```
- 초기화 및 프로젝트 루트 경로 설정

```python
def is_licensed(self) -> bool
```
- 라이선스 유효 여부 확인
- Returns: 라이선스 유효 시 True

```python
def validate_serial(self, serial: str) -> Tuple[bool, str]
```
- 시리얼 번호 형식 검증 (XXXX-XXXX-XXXX-XXXX)
- Args: serial (시리얼 번호)
- Returns: (검증 성공 여부, 메시지)

```python
def activate_license(self, serial: str) -> Tuple[bool, str]
```
- 라이선스 활성화 (서버 인증 시뮬레이션)
- Args: serial (시리얼 번호)
- Returns: (활성화 성공 여부, 메시지)
- 테스트 시리얼: `TEST-1234-5678-ABCD`, `DEMO-0000-0000-0001`

```python
def deactivate_license(self) -> None
```
- 라이선스 비활성화 (파일 삭제)

---

#### `PdfDocumentManager`

PDF 문서 로드, 렌더링, 마스킹 적용을 담당합니다.

**속성**:
- `doc`: fitz.Document 객체
- `file_path`: 현재 열린 PDF 파일 경로

**메서드**:

```python
def __init__(self) -> None
```
- 초기화

```python
def load_pdf(self, path: str) -> None
```
- PDF 파일 로드
- Args: path (PDF 파일 경로)
- Raises: Exception (로드 실패 시)

```python
def get_page_count(self) -> int
```
- 전체 페이지 수 반환
- Returns: 페이지 수

```python
def get_page_pixmap(self, page_index: int, zoom: float = 1.5) -> Optional[QPixmap]
```
- 지정된 페이지를 QPixmap으로 렌더링
- Args: 
  - page_index (페이지 인덱스, 0-based)
  - zoom (확대/축소 배율)
- Returns: QPixmap 객체 또는 None

```python
def apply_masks_and_save(self, masks: List[MaskEntry]) -> None
```
- 마스킹을 PDF에 적용하고 저장 (PyMuPDF Redaction 사용)
- Args: masks (마스킹 정보 리스트)
- Raises: Exception (저장 실패 시)

```python
def close(self) -> None
```
- 문서 닫기

---

#### `MaskDataManager`

마스킹 데이터를 일자별 JSON 파일로 저장/로드합니다.

**속성**:
- `project_root`: 프로젝트 루트 경로
- `masks_dir`: 마스킹 데이터 폴더 경로 (masks_data/)

**메서드**:

```python
def __init__(self) -> None
```
- 초기화 및 폴더 생성

```python
def get_mask_file_path(self) -> str
```
- 일자별 마스킹 데이터 파일 경로 반환
- Returns: masks_data/mask_data_YYYYMMDD.json

```python
def save_masks(self, pdf_path: str, masks: List[MaskEntry]) -> Tuple[bool, str]
```
- 마스킹 데이터를 JSON 파일에 저장
- Args:
  - pdf_path (PDF 파일 경로)
  - masks (마스킹 데이터 리스트)
- Returns: (성공 여부, 메시지 또는 파일 경로)

```python
def load_masks(self, pdf_path: str) -> Tuple[bool, List[MaskEntry], str]
```
- JSON 파일에서 마스킹 데이터 로드
- Args: pdf_path (PDF 파일 경로)
- Returns: (성공 여부, 마스킹 리스트, 메시지)

```python
def delete_masks(self, pdf_path: str) -> Tuple[bool, str]
```
- JSON 파일에서 특정 PDF의 마스킹 데이터 삭제
- Args: pdf_path (PDF 파일 경로)
- Returns: (성공 여부, 메시지)

---

#### `ProgressManager`

폴더 일괄 작업 시 진행상황을 추적합니다.

**속성**:
- `project_root`: 프로젝트 루트 경로
- `progress_file`: 진행상황 파일 경로 (progress.json)

**메서드**:

```python
def __init__(self) -> None
```
- 초기화

```python
def save_progress(
    self,
    folder_path: str,
    pdf_files: List[str],
    completed_files: List[str],
    current_index: int
) -> Tuple[bool, str]
```
- 작업 진행상황 저장
- Args:
  - folder_path (작업 중인 폴더 경로)
  - pdf_files (전체 PDF 파일 리스트)
  - completed_files (완료된 파일 리스트)
  - current_index (현재 작업 중인 파일 인덱스)
- Returns: (성공 여부, 메시지)

```python
def load_progress(self) -> Tuple[bool, Dict, str]
```
- 작업 진행상황 로드
- Returns: (성공 여부, 진행상황 데이터, 메시지)

```python
def clear_progress(self) -> Tuple[bool, str]
```
- 작업 진행상황 삭제
- Returns: (성공 여부, 메시지)

---

#### `LogManager`

애플리케이션 로그를 일자별로 기록합니다.

**속성**:
- `project_root`: 프로젝트 루트 경로
- `logs_dir`: 로그 폴더 경로 (logs/)
- `logger`: Python logging.Logger 객체

**메서드**:

```python
def __init__(self) -> None
```
- 초기화 및 로거 설정

```python
def setup_logger(self) -> None
```
- 일자별 로그 파일 설정 (pdfmask_YYYYMMDD.log)

```python
def info(self, message: str) -> None
```
- 정보 로그 기록

```python
def warning(self, message: str) -> None
```
- 경고 로그 기록

```python
def error(self, message: str) -> None
```
- 에러 로그 기록

```python
def log_app_start(self) -> None
```
- 프로그램 시작 로그

```python
def log_app_end(self) -> None
```
- 프로그램 종료 로그

```python
def log_license_check(self, success: bool, message: str) -> None
```
- 라이선스 인증 로그
- Args:
  - success (인증 성공 여부)
  - message (메시지)

```python
def log_pdf_open(self, file_path: str) -> None
```
- PDF 파일 열기 로그

```python
def log_folder_open(self, folder_path: str, file_count: int) -> None
```
- 폴더 열기 로그

```python
def log_mask_save(self, file_path: str, masks: List[MaskEntry]) -> None
```
- 마스킹 저장 로그 (상세 좌표 포함)

```python
def log_error(self, operation: str, error_message: str) -> None
```
- 에러 로그

---

### UI Module

#### `MainWindow`

메인 애플리케이션 윈도우입니다.

**속성**:
- `pdf_manager`: PdfDocumentManager 인스턴스
- `mask_data_manager`: MaskDataManager 인스턴스
- `progress_manager`: ProgressManager 인스턴스
- `log_manager`: LogManager 인스턴스
- `masks`: 현재 마스킹 데이터 리스트
- `pdf_files`: 폴더 내 PDF 파일 목록
- `current_pdf_index`: 현재 PDF 파일 인덱스
- `completed_files`: 완료된 파일 리스트
- `backup_enabled`: 백업 활성화 여부

**주요 메서드**:

```python
def __init__(self) -> None
```
- 초기화 및 UI 설정

```python
def init_ui(self) -> None
```
- UI 레이아웃 초기화

```python
def setup_menu(self) -> None
```
- 메뉴바 설정 (파일, 설정, 보기, 도움말)

```python
def setup_toolbar(self) -> None
```
- 툴바 설정 (PDF 열기, 폴더 열기)

```python
def setup_shortcuts(self) -> None
```
- 키보드 단축키 설정

```python
def update_page_view(self) -> None
```
- 현재 페이지를 화면에 표시

```python
def open_pdf(self) -> None
```
- PDF 파일 열기 (파일 다이얼로그)

```python
def open_folder(self) -> None
```
- 폴더 열기 및 PDF 파일 목록 로드

```python
def save_masks(self) -> None
```
- 마스킹 정보 저장 (Ctrl+S)
- 백업 → JSON 저장 → Redaction 적용 → 엑셀 저장 → 로그 기록

```python
def backup_current_pdf(self) -> Tuple[bool, str]
```
- 현재 PDF 파일을 백업 폴더에 복사
- Returns: (성공 여부, 메시지 또는 백업 경로)

```python
def export_masks_to_excel(self) -> None
```
- 마스킹 작업 내역을 엑셀 파일로 저장

```python
def on_mask_created(self, page_index: int, rect: fitz.Rect) -> None
```
- 마스킹 영역 생성 시 호출되는 슬롯
- Args:
  - page_index (페이지 인덱스)
  - rect (마스킹 영역 좌표)

```python
def closeEvent(self, event) -> None
```
- 윈도우 종료 이벤트 (로그 기록 및 PDF 닫기)

---

#### `PdfPageView`

PDF 페이지를 표시하고 마스킹 영역을 선택할 수 있는 커스텀 위젯입니다.

**시그널**:
- `maskCreated = pyqtSignal(int, object)`: 마스킹 영역 생성 시 발생

**속성**:
- `_pixmap`: 렌더링된 페이지 이미지
- `_page_index`: 현재 페이지 인덱스
- `_page_width`, `_page_height`: PDF 페이지 실제 크기
- `_saved_masks`: 저장된 마스킹 영역 (화면 좌표)

**주요 메서드**:

```python
def set_page(
    self,
    page_index: int,
    pixmap: QPixmap,
    page_width: float,
    page_height: float,
    masks: List = None
) -> None
```
- 페이지 정보 설정 및 렌더링

```python
def mousePressEvent(self, event) -> None
```
- 마우스 클릭 시작 (Ctrl + 좌클릭)

```python
def mouseMoveEvent(self, event) -> None
```
- 마우스 드래그 중 (실시간 미리보기)

```python
def mouseReleaseEvent(self, event) -> None
```
- 마우스 클릭 종료 (마스킹 영역 확정 및 시그널 발생)

```python
def _convert_to_pdf_rect(self, screen_rect: QRect) -> Optional[fitz.Rect]
```
- 화면 좌표를 PDF 좌표로 변환

```python
def _convert_to_screen_rect(self, pdf_rect: fitz.Rect) -> Optional[QRect]
```
- PDF 좌표를 화면 좌표로 변환

---

#### `ScrollablePdfView`

스크롤 가능한 PDF 뷰 컨테이너입니다.

**속성**:
- `pdf_view`: PdfPageView 인스턴스
- `zoom_level`: 현재 줌 레벨 (1.0 = 100%)
- `min_zoom`, `max_zoom`: 최소/최대 줌 레벨

**주요 메서드**:

```python
def zoom_in(self) -> None
```
- 줌 인 (10% 증가)

```python
def zoom_out(self) -> None
```
- 줌 아웃 (10% 감소)

```python
def wheelEvent(self, event) -> None
```
- 마우스 휠 이벤트 (Ctrl + 휠로 줌)

---

#### `SerialInputDialog`

라이선스 시리얼 번호 입력 다이얼로그입니다.

**속성**:
- `license_manager`: LicenseManager 인스턴스
- `serial_input`: 시리얼 번호 입력 필드
- `status_label`: 상태 메시지 레이블

**주요 메서드**:

```python
def __init__(self, parent: Optional[QWidget] = None) -> None
```
- 초기화 및 UI 설정

```python
def activate(self) -> None
```
- 인증 버튼 클릭 시 호출
- 시리얼 번호 검증 및 라이선스 활성화

---

## 데이터 흐름

### 1. 애플리케이션 시작

```
main.py
  ↓
LicenseManager.is_licensed()
  ↓ (라이선스 없음)
SerialInputDialog.exec()
  ↓ (인증 성공)
MainWindow.show()
```

### 2. PDF 파일 열기

```
MainWindow.open_pdf()
  ↓
PdfDocumentManager.load_pdf()
  ↓
MaskDataManager.load_masks() (저장된 마스킹 로드)
  ↓
MainWindow.update_page_view()
  ↓
PdfDocumentManager.get_page_pixmap()
  ↓
PdfPageView.set_page()
```

### 3. 마스킹 영역 선택

```
사용자: Ctrl + 드래그
  ↓
PdfPageView.mousePressEvent()
  ↓
PdfPageView.mouseMoveEvent() (실시간 미리보기)
  ↓
PdfPageView.mouseReleaseEvent()
  ↓
PdfPageView.maskCreated 시그널 발생
  ↓
MainWindow.on_mask_created()
  ↓
masks 리스트에 MaskEntry 추가
  ↓
mask_list 테이블에 행 추가
```

### 4. 마스킹 저장

```
사용자: Ctrl + S
  ↓
MainWindow.save_masks()
  ↓
(백업 활성화 시) MainWindow.backup_current_pdf()
  ↓
MaskDataManager.save_masks() (JSON 저장)
  ↓
PdfDocumentManager.apply_masks_and_save() (Redaction 적용)
  ↓
MainWindow.export_masks_to_excel()
  ↓
LogManager.log_mask_save()
  ↓
ProgressManager.save_progress()
  ↓
다음 파일로 이동 확인
```

### 5. 폴더 일괄 처리

```
MainWindow.open_folder()
  ↓
ProgressManager.load_progress() (이전 진행상황 확인)
  ↓
pdf_files 리스트 생성
  ↓
첫 번째 (또는 복구된) PDF 로드
  ↓
사용자: 마스킹 작업
  ↓
MainWindow.save_masks()
  ↓
다음 PDF 자동 이동
  ↓
반복...
  ↓
모든 파일 완료 시 ProgressManager.clear_progress()
```

---

## 실행 방법

### 1. 의존성 설치

```bash
uv sync
```

### 2. 프로그램 실행

```bash
# 방법 1: uv를 통한 실행
uv run python src/main.py

# 방법 2: 직접 실행 (가상환경 활성화 후)
python src/main.py

# 방법 3: 스크립트로 실행 (pyproject.toml 설정 후)
uv run pdfmask
```

### 3. 첫 실행 시

- 라이선스 인증 다이얼로그가 표시됩니다.
- 테스트 시리얼 번호:
  - `TEST-1234-5678-ABCD`
  - `DEMO-0000-0000-0001`

### 4. 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+O` | PDF 열기 |
| `Ctrl+Shift+O` | 폴더 열기 |
| `Ctrl+S` | 마스킹 저장 |
| `Ctrl+드래그` | 마스킹 영역 선택 |
| `Ctrl+휠` | 확대/축소 (50%~200%) |
| `←` / `→` | 이전/다음 페이지 |
| `Del` | 마스킹 삭제 |
| `더블클릭` | 메모 편집 |

---

## 파일 포맷

### 1. 마스킹 데이터 JSON (`masks_data/mask_data_YYYYMMDD.json`)

```json
{
  "date": "2025-11-19",
  "files": [
    {
      "pdf_file": "example.pdf",
      "saved_at": "2025-11-19T10:30:00",
      "mask_count": 2,
      "masks": [
        {
          "page_index": 0,
          "rect": {
            "x0": 100.0,
            "y0": 200.0,
            "x1": 300.0,
            "y1": 250.0
          },
          "note": "주민번호"
        }
      ]
    }
  ]
}
```

### 2. 진행상황 JSON (`progress.json`)

```json
{
  "folder_path": "C:/Documents/PDFs",
  "last_updated": "2025-11-19T10:30:00",
  "total_files": 10,
  "completed_count": 5,
  "current_index": 5,
  "pdf_files": ["file1.pdf", "file2.pdf", ...],
  "completed_files": ["file1.pdf", "file2.pdf", ...]
}
```

### 3. 라이선스 JSON (`.license`)

```json
{
  "activated": true,
  "serial": "TEST-1234-5678-ABCD",
  "serial_hash": "abc123...",
  "activated_at": "2025-11-19T10:00:00"
}
```

### 4. 로그 파일 (`logs/pdfmask_YYYYMMDD.log`)

```
2025-11-19 10:00:00 - INFO - ============================================================
2025-11-19 10:00:00 - INFO - PDF Mask Application Started
2025-11-19 10:00:00 - INFO - ============================================================
2025-11-19 10:00:05 - INFO - License Check: SUCCESS - License verified
2025-11-19 10:01:00 - INFO - PDF Opened: C:/Documents/example.pdf
2025-11-19 10:05:00 - INFO - Mask Saved: C:/Documents/example.pdf (2 masks)
2025-11-19 10:05:00 - INFO -   Mask #1: Page 1, Rect(100.00, 200.00, 300.00, 250.00), Note: 주민번호
```

---

## 확장 가능성

### 1. 추가 기능 제안

- **마스킹 템플릿**: 자주 사용하는 마스킹 패턴 저장
- **OCR 연동**: 텍스트 자동 인식 및 마스킹
- **일괄 마스킹**: 동일한 텍스트를 전체 페이지에서 자동 마스킹
- **클라우드 동기화**: 마스킹 데이터 클라우드 백업

### 2. 코드 확장 방법

**새로운 관리자 클래스 추가**:
```python
# src/pdfmask/managers/template_manager.py
class TemplateManager:
    def save_template(self, name: str, masks: List[MaskEntry]) -> bool:
        # 템플릿 저장 로직
        pass
    
    def load_template(self, name: str) -> List[MaskEntry]:
        # 템플릿 로드 로직
        pass
```

**새로운 UI 컴포넌트 추가**:
```python
# src/pdfmask/ui/template_dialog.py
class TemplateDialog(QDialog):
    def __init__(self, parent=None):
        # 템플릿 관리 다이얼로그
        pass
```

**유틸리티 함수 추가**:
```python
# src/pdfmask/utils/text_utils.py
def find_text_in_pdf(doc: fitz.Document, search_text: str) -> List[fitz.Rect]:
    # PDF에서 텍스트 검색 및 위치 반환
    pass
```

---

## 주의사항

### 1. PDF 파일 처리

- **영구 마스킹**: Redaction은 복구 불가능합니다. 백업 기능을 활성화하세요.
- **파일 잠금**: PDF를 다른 프로그램에서 닫고 저장하세요.
- **대용량 파일**: 4GB 이상 메모리 권장

### 2. 백업 관리

- 백업 폴더는 자동으로 생성되며, 일자별로 구분됩니다.
- 디스크 공간을 확인하세요.

### 3. 라이선스

- `.license` 파일을 삭제하면 재인증이 필요합니다.
- 실제 배포 시 서버 인증 API를 구현하세요.

---

## 문제 해결

| 문제 | 해결 |
|------|------|
| "Permission denied" | PDF를 다른 프로그램에서 닫기 |
| 확대/축소 안됨 | `Ctrl` 키 누른 상태에서 휠 |
| 마스킹 드래그 안됨 | `Ctrl` 키 누른 상태에서 드래그 |
| 독 위젯 재결합 안됨 | 창 최대화 해제 후 재시도 |

---

## 버전 히스토리

### v1.5.0 (2025-11-19)

- ✨ 프로젝트 모듈화 및 구조 개선
- ✨ 코드 분리: core, managers, ui, utils
- ✨ 기능 명세서 작성

### v1.5 (2025-11-18)

- ✨ PDF 자동 백업 / 라이선스 인증
- ✨ 마스킹 데이터 JSON / 진행 상황 추적
- ✨ 상세 로그 기록 (좌표 포함)

### v1.0 (2025-11-17)

- 🎉 첫 번째 정식 릴리스

---

## 라이선스 및 기여

- **라이선스**: 자유롭게 사용 가능
- **기여**: 버그 리포트, 기능 제안 환영
- **문의**: GitHub Issues 또는 이메일

---

**PDF Mask v1.5** - 빠르고 안전한 PDF 개인정보 마스킹 솔루션

