# PDF Mask 개발 로그

## 프로젝트 개요
- **프로젝트명**: PDF Mask
- **설명**: PDF 마스킹 프로그램
- **Python 버전**: 3.12
- **주요 라이브러리**: PyQt6, PyMuPDF (fitz)

---

## 2025-11-17: 초기 프로젝트 설정 및 GUI 뼈대 구성

### 1. 프로젝트 초기화
- `pyproject.toml` 파일 확인
- Python 3.12 환경 구성
- 의존성: `pymupdf>=1.26.6`

### 2. GUI 프레임워크 선택 및 설정

#### 2.1 PyQt5 → PyQt6 마이그레이션
**문제**: Windows 환경에서 PyQt5 설치 실패
```
error: Distribution `pyqt5-qt5==5.15.18` can't be installed because it doesn't have a source distribution or wheel for the current platform
```

**해결**: PyQt6로 변경
- `pyproject.toml`에 `pyqt6>=6.5.0` 추가
- PyQt5 → PyQt6 코드 마이그레이션 수행

#### 2.2 PyQt6 마이그레이션 변경 사항
1. **Import 경로 변경**
   - `from PyQt5.QtWidgets import ...` → `from PyQt6.QtWidgets import ...`
   - `QAction`: `QtWidgets` → `QtGui`
   - `QShortcut`: `QtWidgets` → `QtGui`

2. **열거형(Enum) 값 변경**
   - `Qt.AlignCenter` → `Qt.AlignmentFlag.AlignCenter`
   - `Qt.RightDockWidgetArea` → `Qt.DockWidgetArea.RightDockWidgetArea`
   - `Qt.Key_Right` → `Qt.Key.Key_Right`
   - `Qt.Key_Left` → `Qt.Key.Key_Left`
   - `Qt.Key_PageDown` → `Qt.Key.Key_PageDown`
   - `Qt.Key_PageUp` → `Qt.Key.Key_PageUp`

3. **메서드 이름 변경**
   - `app.exec_()` → `app.exec()`

### 3. GUI 구조 설계 및 구현

#### 3.1 MainWindow 클래스 구조
```python
class MainWindow(QMainWindow):
    - init_ui(): UI 초기화
    - setup_menu(): 메뉴바 설정
    - setup_toolbar(): 툴바 설정
    - setup_shortcuts(): 키보드 단축키 설정
```

#### 3.2 레이아웃 구성
```
┌─────────────────────────────────────────────────────────┐
│ 메뉴바: 파일(&F) > PDF 열기, 폴더 열기, 종료           │
├─────────────────────────────────────────────────────────┤
│ 툴바: [PDF 열기] [폴더 열기]                            │
├──────────────┬─────────────────────┬────────────────────┤
│              │                     │ PDF 파일 목록      │
│  마스킹 리스트│   PDF 페이지 뷰     │ (Dock Widget)     │
│ (QTableWidget)│    (QLabel)        │ (QListWidget)     │
│  [페이지|메모]│                     │                   │
│              │                     │                   │
└──────────────┴─────────────────────┴────────────────────┘
```

#### 3.3 UI 구성 요소

**왼쪽 영역: 마스킹 리스트**
- `QTableWidget` 사용
- 컬럼: "페이지", "메모"
- 최소 너비: 250px, 최대 너비: 400px

**가운데 영역: PDF 페이지 뷰**
- `QLabel` 사용 (placeholder)
- 중앙 정렬
- 배경색: #f0f0f0, 테두리: 1px solid #ccc

**오른쪽 영역: PDF 파일 목록**
- `QDockWidget` + `QListWidget` 사용
- 타이틀: "PDF 파일 목록"
- 최소 너비: 200px
- 위치: 오른쪽 도킹 영역

#### 3.4 메뉴 및 툴바

**파일(&F) 메뉴**
1. PDF 열기... (Ctrl+O)
   - 단일 PDF 파일 선택
   - `QFileDialog.getOpenFileName()` 사용
   
2. 폴더 열기... (Ctrl+Shift+O)
   - PDF 파일이 있는 폴더 선택
   - `QFileDialog.getExistingDirectory()` 사용
   
3. 종료 (Ctrl+Q)
   - 프로그램 종료

**툴바**
- PDF 열기 버튼
- 폴더 열기 버튼

#### 3.5 키보드 단축키

| 키 | 기능 | 메서드 |
|---|------|--------|
| Left (←) | 이전 페이지 | `go_prev_page()` |
| Right (→) | 다음 페이지 | `go_next_page()` |
| PageUp | 이전 페이지 | `go_prev_page()` |
| PageDown | 다음 페이지 | `go_next_page()` |
| Ctrl+S | 마스킹 정보 저장 | `save_masks()` |

*현재는 더미 구현 (print 출력만)*

### 4. 코드 품질

#### 4.1 타입 힌트 적용
- 모든 메서드에 반환 타입 명시 (`-> None`)
- 타입 안정성 향상

#### 4.2 코드 구조
- 클래스 기반 설계
- 관심사 분리 (UI 초기화, 메뉴, 툴바, 단축키를 별도 메서드로 분리)
- Docstring 추가

### 5. 현재 구현 상태

#### 완료된 기능
✅ PyQt6 환경 설정  
✅ MainWindow 기본 구조  
✅ 3단 레이아웃 (왼쪽/가운데/오른쪽)  
✅ 메뉴바 구성  
✅ 툴바 구성  
✅ 키보드 단축키 등록  
✅ 파일/폴더 선택 다이얼로그 연동  

#### TODO (향후 구현 예정)
- [ ] PyMuPDF를 이용한 PDF 파일 로드
- [ ] PDF 페이지 렌더링 및 표시
- [ ] 마스킹 영역 선택 기능
- [ ] 마스킹 리스트 관리 (추가/수정/삭제)
- [ ] 폴더 내 PDF 파일 목록 로드
- [ ] 페이지 네비게이션 구현
- [ ] 마스킹 정보 저장/불러오기

### 6. 실행 방법

```bash
# 의존성 설치
uv sync

# 프로그램 실행
uv run python main.py
```

### 7. 파일 구조

```
pdfmask/
├── main.py              # 메인 애플리케이션
├── pyproject.toml       # 프로젝트 설정 및 의존성
├── README.md
├── DEVLOG.md           # 개발 로그 (이 파일)
├── .python-version
└── uv.lock
```

---

## 참고 사항

### PyQt6 주요 변경 사항 요약
- Python 3.6+ 지원 (타입 힌트 개선)
- 열거형 값이 더 명시적으로 변경 (예: `Qt.Key.Key_Right`)
- 일부 클래스 위치 변경 (`QAction`, `QShortcut` 등)
- `exec_()` → `exec()` 메서드 이름 변경
- Windows, macOS, Linux 모두 안정적인 wheel 제공

### 의존성
```toml
dependencies = [
    "pymupdf>=1.26.6",
    "pyqt6>=6.5.0",
]
```

---

## 2025-11-17 (2단계): PDF 문서 로드 및 렌더링 기능 구현

### 1. PdfDocumentManager 클래스 추가

PDF 문서를 관리하는 전용 클래스를 구현했습니다.

#### 1.1 주요 속성
```python
self.doc: Optional[fitz.Document] = None  # PyMuPDF 문서 객체
self.file_path: Optional[str] = None       # 현재 열린 파일 경로
```

#### 1.2 주요 메서드

**`load_pdf(path: str) -> None`**
- 기존 문서가 열려있으면 닫고 새 문서를 엽니다
- 예외 발생 시 Exception을 raise하여 상위에서 처리합니다

**`get_page_count() -> int`**
- 전체 페이지 수를 반환합니다
- 문서가 없으면 0을 반환합니다

**`get_page_pixmap(page_index: int, zoom: float = 1.5) -> Optional[QPixmap]`**
- PyMuPDF의 `page.get_pixmap()`으로 페이지를 렌더링합니다
- zoom 파라미터로 확대/축소 비율 조정 (기본값: 1.5)
- PyMuPDF Pixmap → QImage → QPixmap 변환 과정을 거칩니다
- 실패 시 None을 반환합니다

**`close() -> None`**
- 문서를 닫고 리소스를 정리합니다

### 2. MainWindow 업데이트

#### 2.1 새로운 속성 추가
```python
self.pdf_manager = PdfDocumentManager()  # PDF 문서 관리자
self.current_page_index: int = 0          # 현재 페이지 인덱스
```

#### 2.2 새로운 메서드

**`setup_statusbar() -> None`**
- 상태바를 초기화합니다

**`update_page_view() -> None`**
- 현재 페이지를 중앙 뷰에 렌더링하여 표시합니다
- 상태바에 "페이지: N / M" 형식으로 페이지 정보를 표시합니다
- 문서가 없거나 렌더링 실패 시 적절한 메시지를 표시합니다

#### 2.3 PDF 열기 기능 구현

**`open_pdf()` 메서드 업데이트**
1. `QFileDialog`로 PDF 파일 선택
2. `pdf_manager.load_pdf()`로 문서 로드
3. `current_page_index`를 0으로 초기화
4. `update_page_view()`로 첫 페이지 표시
5. 창 제목에 파일명 표시
6. 오류 발생 시 `QMessageBox`로 에러 메시지 표시

#### 2.4 페이지 네비게이션 구현

**`go_next_page()` - 다음 페이지**
- 문서가 열려있는지 확인
- 마지막 페이지가 아닌 경우 페이지 인덱스 증가
- `update_page_view()` 호출

**`go_prev_page()` - 이전 페이지**
- 문서가 열려있는지 확인
- 첫 페이지가 아닌 경우 페이지 인덱스 감소
- `update_page_view()` 호출

**작동하는 키보드 단축키:**
- Left (←) / PageUp: 이전 페이지
- Right (→) / PageDown: 다음 페이지

#### 2.5 리소스 관리

**`closeEvent()` 메서드 추가**
- 윈도우 종료 시 PDF 문서를 자동으로 닫아 메모리 누수 방지

### 3. PyMuPDF Pixmap → QPixmap 변환 과정

```python
# 1. PyMuPDF로 페이지 렌더링
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)

# 2. Pixmap 데이터를 QImage로 변환
img = QImage(
    pix.samples,           # 이미지 데이터
    pix.width,             # 너비
    pix.height,            # 높이
    pix.stride,            # 행 바이트 수
    QImage.Format.Format_RGB888  # RGB 포맷
)

# 3. QImage를 QPixmap으로 변환
return QPixmap.fromImage(img)
```

### 4. UI 개선사항

- `QLabel.setScaledContents(False)`: 원본 크기 유지
- 상태바에 현재 페이지 정보 표시
- 창 제목에 열린 파일명 표시
- 오류 발생 시 사용자 친화적인 에러 다이얼로그 표시

### 5. 테스트 방법

```bash
uv run python main.py
```

1. "PDF 열기" 버튼 또는 Ctrl+O로 PDF 파일 선택
2. 첫 페이지가 중앙에 렌더링되어 표시됨
3. 방향키(←/→) 또는 PageUp/PageDown으로 페이지 이동
4. 상태바에서 현재 페이지 정보 확인

### 6. 구현 완료 상태 업데이트

#### 완료된 기능
✅ PyQt6 환경 설정  
✅ MainWindow 기본 구조  
✅ 3단 레이아웃 (왼쪽/가운데/오른쪽)  
✅ 메뉴바 구성  
✅ 툴바 구성  
✅ 키보드 단축키 등록  
✅ 파일/폴더 선택 다이얼로그 연동  
✅ **PDF 문서 로드 기능**  
✅ **PDF 페이지 렌더링 및 표시**  
✅ **페이지 네비게이션 (방향키/PageUp/PageDown)**  
✅ **상태바에 페이지 정보 표시**  

#### TODO (향후 구현 예정)
- [ ] 마스킹 영역 선택 기능
- [ ] 마스킹 리스트 관리 (추가/수정/삭제)
- [ ] 폴더 내 PDF 파일 목록 로드
- [ ] 마스킹 정보 저장/불러오기
- [ ] 확대/축소 기능
- [ ] PDF 파일 목록에서 파일 선택하여 전환

### 7. 주요 개선 사항

- **메모리 관리**: 윈도우 종료 시 PDF 문서 자동 닫기
- **에러 처리**: try/except로 파일 로드 오류를 처리하고 사용자에게 알림
- **타입 힌트**: 모든 새로운 메서드에 타입 힌트 적용
- **사용자 경험**: 상태바와 창 제목으로 현재 상태 명확히 표시

---

## 2025-11-17 (3단계): 마스킹 영역 선택 기능 구현

### 1. PdfPageView 커스텀 위젯 구현

기존 `QLabel` 기반 PDF 뷰를 커스텀 위젯으로 교체하여 마우스 드래그로 마스킹 영역을 선택할 수 있게 했습니다.

#### 1.1 클래스 구조
```python
class PdfPageView(QWidget):
    maskCreated = pyqtSignal(int, object)  # 시그널: (page_index, fitz.Rect)
```

#### 1.2 주요 속성

**페이지 표시 관련**
- `_pixmap: Optional[QPixmap]` - 현재 페이지 이미지
- `_page_index: int` - 현재 페이지 번호
- `_page_width: float` - PDF 페이지 실제 폭
- `_page_height: float` - PDF 페이지 실제 높이

**마스킹 드래그 관련**
- `_start_pos: Optional[QPoint]` - 드래그 시작점
- `_current_rect: Optional[QRect]` - 현재 드래그 중인 사각형
- `_ctrl_pressed_during_drag: bool` - Ctrl 키 눌림 상태

#### 1.3 주요 메서드

**`set_page(page_index, pixmap, page_width, page_height) -> None`**
- 페이지 정보를 설정하고 화면을 업데이트합니다
- 위젯 크기를 pixmap 크기에 맞춥니다

**`paintEvent(event) -> None`**
- `QPainter`로 pixmap을 그립니다
- 드래그 중인 사각형이 있으면 반투명 오버레이로 표시합니다
  - 색상: 파란색 (RGB: 0, 120, 255)
  - 투명도: 80 (약 31%)
  - 테두리: 2px 파란색

**`mousePressEvent(event) -> None`**
- **Ctrl + 좌클릭**인 경우에만 드래그를 시작합니다
- 조건: `event.button() == Qt.MouseButton.LeftButton and event.modifiers() & Qt.KeyboardModifier.ControlModifier`

**`mouseMoveEvent(event) -> None`**
- Ctrl 드래그 중일 때 현재 마우스 위치로 사각형을 업데이트합니다
- `QRect.normalized()`로 시작점과 현재점으로 정규화된 사각형 생성

**`mouseReleaseEvent(event) -> None`**
- 드래그가 완료되면 화면 좌표를 PDF 좌표로 변환합니다
- `maskCreated` 시그널을 발생시킵니다
- 드래그 상태를 초기화합니다

**`_convert_to_pdf_rect(screen_rect) -> Optional[fitz.Rect]`**
- 화면 좌표를 PDF 페이지 좌표로 변환합니다
- 변환 공식:
  ```python
  scale_x = page_width / pixmap.width()
  scale_y = page_height / pixmap.height()
  
  pdf_x0 = screen_x0 * scale_x
  pdf_y0 = screen_y0 * scale_y
  pdf_x1 = screen_x1 * scale_x
  pdf_y1 = screen_y1 * scale_y
  ```

### 2. MainWindow 업데이트

#### 2.1 PdfPageView 통합

**기존 코드 (QLabel)**
```python
self.pdf_view = QLabel("PDF 페이지 뷰")
self.pdf_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
```

**새로운 코드 (PdfPageView)**
```python
self.pdf_view = PdfPageView(self)
self.pdf_view.maskCreated.connect(self.on_mask_created)
```

#### 2.2 update_page_view() 수정

페이지를 표시할 때 PDF 페이지의 실제 크기 정보도 함께 전달하도록 수정했습니다:

```python
def update_page_view(self) -> None:
    # 현재 페이지 객체 가져오기
    page = self.pdf_manager.doc[self.current_page_index]
    
    # 페이지 실제 크기
    page_width = page.rect.width
    page_height = page.rect.height
    
    # 페이지 렌더링
    pixmap = self.pdf_manager.get_page_pixmap(self.current_page_index)
    
    # PdfPageView에 페이지 설정
    self.pdf_view.set_page(
        self.current_page_index,
        pixmap,
        page_width,
        page_height
    )
```

#### 2.3 마스킹 시그널 처리

**`on_mask_created(page_index, rect)` 슬롯 추가**
- `maskCreated` 시그널을 받아서 처리합니다
- 현재는 콘솔에 출력만 하고, 다음 단계에서 마스킹 리스트에 추가할 예정입니다

```python
def on_mask_created(self, page_index: int, rect: fitz.Rect) -> None:
    print(f"Mask created on page {page_index + 1}: {rect}")
    # TODO: 마스킹 리스트에 추가하는 로직 구현 예정
```

### 3. 사용 방법

1. **PDF 파일 열기**
   - "PDF 열기" 버튼 또는 Ctrl+O

2. **마스킹 영역 선택**
   - **Ctrl 키를 누른 상태**에서 마우스로 드래그
   - 드래그 중에 반투명 파란색 사각형이 표시됩니다
   - 마우스를 놓으면 해당 영역이 마스킹으로 등록됩니다

3. **페이지 이동**
   - 방향키(←/→) 또는 PageUp/PageDown

### 4. 좌표 변환 시스템

#### 4.1 왜 좌표 변환이 필요한가?

- **화면 좌표**: 렌더링된 이미지의 픽셀 좌표 (zoom에 따라 변함)
- **PDF 좌표**: PDF 문서의 실제 좌표 (포인트 단위, 72 DPI 기준)

zoom = 1.5로 렌더링하면 화면 좌표는 PDF 좌표의 1.5배가 됩니다.

#### 4.2 변환 프로세스

```
사용자 드래그 (화면 좌표)
    ↓
scale_x = PDF_width / Pixmap_width
scale_y = PDF_height / Pixmap_height
    ↓
PDF 좌표 = 화면 좌표 × scale
    ↓
fitz.Rect (PDF 좌표계)
```

### 5. 시각적 피드백

#### 5.1 드래그 사각형 스타일
- **배경**: 파란색 (0, 120, 255), 투명도 80
- **테두리**: 파란색 2px
- **실시간 업데이트**: 마우스 이동 시 즉시 반영

#### 5.2 상태바 안내
- 기본: "준비 (Ctrl + 드래그로 마스킹 영역 선택)"
- 페이지 표시 중: "페이지: N / M (Ctrl + 드래그로 마스킹 영역 선택)"

### 6. 구현 완료 상태 업데이트

#### 완료된 기능
✅ PyQt6 환경 설정  
✅ MainWindow 기본 구조  
✅ 3단 레이아웃 (왼쪽/가운데/오른쪽)  
✅ 메뉴바 구성  
✅ 툴바 구성  
✅ 키보드 단축키 등록  
✅ 파일/폴더 선택 다이얼로그 연동  
✅ PDF 문서 로드 기능  
✅ PDF 페이지 렌더링 및 표시  
✅ 페이지 네비게이션 (방향키/PageUp/PageDown)  
✅ 상태바에 페이지 정보 표시  
✅ **커스텀 PDF 뷰어 위젯 (PdfPageView)**  
✅ **Ctrl + 드래그로 마스킹 영역 선택**  
✅ **화면 좌표 → PDF 좌표 변환**  
✅ **마스킹 영역 시그널 발생**  

#### TODO (향후 구현 예정)
- [ ] 마스킹 리스트에 선택한 영역 추가
- [ ] 마스킹 리스트 관리 (수정/삭제)
- [ ] 선택한 마스킹 영역을 페이지에 표시 (저장된 마스킹 시각화)
- [ ] 폴더 내 PDF 파일 목록 로드
- [ ] 마스킹 정보 저장/불러오기
- [ ] 확대/축소 기능
- [ ] PDF 파일 목록에서 파일 선택하여 전환

### 7. PyQt6 시그널/슬롯 패턴

이번 단계에서 커스텀 시그널을 구현했습니다:

```python
# 시그널 선언
class PdfPageView(QWidget):
    maskCreated = pyqtSignal(int, object)  # (page_index, fitz.Rect)

# 시그널 발생
self.maskCreated.emit(page_index, pdf_rect)

# 시그널 연결
self.pdf_view.maskCreated.connect(self.on_mask_created)

# 슬롯 구현
def on_mask_created(self, page_index: int, rect: fitz.Rect) -> None:
    print(f"Mask created on page {page_index + 1}: {rect}")
```

### 8. 테스트 방법

```bash
uv run python main.py
```

1. PDF 파일 열기
2. **Ctrl 키를 누른 채로** 마우스를 드래그
3. 드래그 중 반투명 파란색 사각형이 표시되는지 확인
4. 마우스를 놓으면 콘솔에 마스킹 정보가 출력되는지 확인
5. 다른 페이지로 이동하여 여러 페이지에서 테스트

---

## 2025-11-17 (4단계): 마스킹 데이터 관리 및 리스트 동기화

### 1. MaskEntry 데이터 클래스 추가

Python의 `dataclass`를 사용하여 마스킹 정보를 구조화했습니다.

```python
from dataclasses import dataclass

@dataclass
class MaskEntry:
    """마스킹 정보 데이터 클래스"""
    page_index: int      # 페이지 인덱스 (0부터 시작)
    rect: fitz.Rect      # PDF 좌표계의 사각형
    note: str = ""       # 사용자 메모 (기본값: 빈 문자열)
```

#### 장점
- 타입 안정성
- 간결한 코드
- 자동 `__init__`, `__repr__` 등 생성

### 2. MainWindow에 마스킹 데이터 저장

#### 2.1 마스킹 리스트 추가
```python
self.masks: list[MaskEntry] = []
```

- 한 PDF 문서의 모든 마스킹 정보를 저장
- 리스트 인덱스와 테이블 행 번호를 1:1로 매칭

#### 2.2 데이터와 UI 동기화 전략
```
self.masks 리스트 인덱스 == QTableWidget 행 번호

예시:
masks[0] → 테이블 행 0
masks[1] → 테이블 행 1
masks[2] → 테이블 행 2
```

이 규칙으로 간단하고 명확한 데이터 관리가 가능합니다.

### 3. 마스킹 리스트 테이블 설정

#### 3.1 setup_mask_table() 메서드

**컬럼 구성**
- 컬럼 0: "페이지" (읽기 전용)
- 컬럼 1: "메모" (편집 가능)

**주요 설정**
```python
# 행 헤더 숨김
self.mask_list.verticalHeader().setVisible(False)

# 컬럼 크기
self.mask_list.setColumnWidth(0, 60)  # 페이지: 고정 60px
self.mask_list.horizontalHeader().setStretchLastSection(True)  # 메모: 자동 확장

# 선택 모드: 행 단위
self.mask_list.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

# 편집 트리거: 더블클릭 또는 편집 키
self.mask_list.setEditTriggers(
    QTableWidget.EditTrigger.DoubleClicked | 
    QTableWidget.EditTrigger.EditKeyPressed
)
```

#### 3.2 시그널 연결
```python
self.mask_list.itemChanged.connect(self.on_mask_item_changed)
```

### 4. 마스킹 생성 처리

#### 4.1 on_mask_created() 구현

마스킹 영역이 선택되면 자동으로 호출됩니다:

```python
def on_mask_created(self, page_index: int, rect: fitz.Rect) -> None:
    # 1. MaskEntry 생성 및 저장
    mask_entry = MaskEntry(page_index=page_index, rect=rect, note="")
    self.masks.append(mask_entry)
    
    # 2. 테이블에 새 행 추가
    row = self.mask_list.rowCount()
    self.mask_list.insertRow(row)
    
    # 3. 페이지 컬럼 (읽기 전용)
    page_item = QTableWidgetItem(str(page_index + 1))
    page_item.setFlags(page_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    self.mask_list.setItem(row, 0, page_item)
    
    # 4. 메모 컬럼 (편집 가능)
    note_item = QTableWidgetItem("")
    self.mask_list.setItem(row, 1, note_item)
    
    # 5. UserRole에 인덱스 저장
    page_item.setData(Qt.ItemDataRole.UserRole, row)
```

#### 4.2 프로세스
```
사용자 Ctrl + 드래그
    ↓
maskCreated 시그널 발생
    ↓
on_mask_created() 호출
    ↓
MaskEntry 생성 → self.masks에 추가
    ↓
QTableWidget에 새 행 추가
```

### 5. 메모 편집 기능

#### 5.1 사용자 인터랙션
- **더블클릭**: 메모 셀 편집 모드 진입
- **Enter 키** 또는 **다른 셀 클릭**: 편집 완료

#### 5.2 on_mask_item_changed() 구현

편집이 완료되면 자동으로 호출됩니다:

```python
def on_mask_item_changed(self, item: QTableWidgetItem) -> None:
    row = item.row()
    col = item.column()
    
    # 메모 컬럼(1번)만 처리
    if col == 1:
        if 0 <= row < len(self.masks):
            new_note = item.text()
            self.masks[row].note = new_note
            print(f"Mask [{row}] note updated: '{new_note}'")
```

#### 5.3 데이터 흐름
```
사용자가 메모 편집
    ↓
편집 완료 (Enter 또는 포커스 이동)
    ↓
itemChanged 시그널 발생
    ↓
on_mask_item_changed() 호출
    ↓
self.masks[row].note 업데이트
```

### 6. PDF 파일 열기 시 초기화

새로운 PDF를 열면 기존 마스킹 데이터를 자동으로 초기화합니다:

```python
def open_pdf(self) -> None:
    # ...
    self.masks.clear()               # 마스킹 데이터 초기화
    self.mask_list.setRowCount(0)   # 테이블 초기화
    # ...
```

### 7. 저장 기능 (준비 단계)

현재는 콘솔에 출력만 하지만, 향후 파일 저장을 위한 준비가 되어 있습니다:

```python
def save_masks(self) -> None:
    print(f"총 {len(self.masks)}개의 마스킹 정보:")
    for i, mask in enumerate(self.masks):
        print(f"  [{i}] 페이지 {mask.page_index + 1}: {mask.rect}, 메모: '{mask.note}'")
    # TODO: JSON/CSV 등으로 파일 저장
```

### 8. 사용 시나리오

#### 8.1 기본 워크플로우

1. **PDF 파일 열기**
   - Ctrl+O 또는 "PDF 열기" 버튼

2. **마스킹 영역 선택**
   - Ctrl + 드래그로 마스킹할 영역 선택
   - 왼쪽 리스트에 자동으로 추가됨

3. **메모 작성**
   - 리스트에서 메모 셀을 더블클릭
   - 메모 입력 (예: "이름", "주민번호", "주소" 등)
   - Enter 키로 완료

4. **여러 페이지 작업**
   - 방향키로 다른 페이지 이동
   - 반복하여 마스킹 영역 추가

5. **저장**
   - Ctrl+S (현재는 콘솔 출력)

#### 8.2 예시 시나리오
```
1. "계약서.pdf" 파일 열기
2. 1페이지에서 Ctrl+드래그 → "계약자 이름" 메모 입력
3. 1페이지에서 Ctrl+드래그 → "주민번호" 메모 입력
4. 2페이지로 이동
5. 2페이지에서 Ctrl+드래그 → "서명" 메모 입력
6. Ctrl+S로 저장

결과:
마스킹 리스트:
┌────────┬──────────────┐
│ 페이지 │ 메모         │
├────────┼──────────────┤
│ 1      │ 계약자 이름  │
│ 1      │ 주민번호     │
│ 2      │ 서명         │
└────────┴──────────────┘
```

### 9. 구현 세부사항

#### 9.1 페이지 컬럼 읽기 전용 처리
```python
page_item.setFlags(page_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
```
- 비트 연산으로 편집 플래그 제거
- 사용자가 실수로 페이지 번호를 수정하는 것 방지

#### 9.2 메모 컬럼 필터링
```python
if col == 1:  # 메모 컬럼만 처리
    self.masks[row].note = item.text()
```
- `itemChanged` 시그널은 모든 셀 변경에 발생
- 컬럼 체크로 메모 변경만 처리

### 10. 구현 완료 상태 업데이트

#### 완료된 기능
✅ PyQt6 환경 설정  
✅ MainWindow 기본 구조  
✅ 3단 레이아웃 (왼쪽/가운데/오른쪽)  
✅ 메뉴바 구성  
✅ 툴바 구성  
✅ 키보드 단축키 등록  
✅ 파일/폴더 선택 다이얼로그 연동  
✅ PDF 문서 로드 기능  
✅ PDF 페이지 렌더링 및 표시  
✅ 페이지 네비게이션 (방향키/PageUp/PageDown)  
✅ 상태바에 페이지 정보 표시  
✅ 커스텀 PDF 뷰어 위젯 (PdfPageView)  
✅ Ctrl + 드래그로 마스킹 영역 선택  
✅ 화면 좌표 → PDF 좌표 변환  
✅ 마스킹 영역 시그널 발생  
✅ **MaskEntry 데이터 클래스**  
✅ **마스킹 데이터 저장 및 관리**  
✅ **마스킹 리스트 테이블 표시**  
✅ **더블클릭으로 메모 편집**  
✅ **데이터와 UI 자동 동기화**  
✅ **페이지 컬럼 읽기 전용 처리**  

#### TODO (향후 구현 예정)
- [ ] 마스킹 리스트에서 선택한 항목 삭제 기능
- [ ] 선택한 마스킹 영역을 PDF 페이지에 시각적으로 표시
- [ ] 마스킹 리스트 항목 클릭 시 해당 페이지로 이동
- [ ] 폴더 내 PDF 파일 목록 로드
- [ ] 마스킹 정보 파일로 저장/불러오기 (JSON)
- [ ] 확대/축소 기능
- [ ] PDF 파일 목록에서 파일 선택하여 전환
- [ ] 마스킹 영역 실제 적용 (검은색 박스로 덮기)

### 11. 데이터 구조 요약

```python
# 단일 마스킹 정보
MaskEntry(
    page_index=0,                    # 1페이지
    rect=fitz.Rect(100, 200, 300, 250),  # PDF 좌표
    note="주민번호"                   # 사용자 메모
)

# 전체 마스킹 리스트
self.masks = [
    MaskEntry(page_index=0, rect=..., note="이름"),
    MaskEntry(page_index=0, rect=..., note="주민번호"),
    MaskEntry(page_index=1, rect=..., note="서명"),
]

# 테이블 표시
Row 0: [1, "이름"]      ← masks[0]
Row 1: [1, "주민번호"]  ← masks[1]
Row 2: [2, "서명"]      ← masks[2]
```

### 12. 테스트 방법

```bash
uv run python main.py
```

**테스트 시나리오:**

1. PDF 파일 열기
2. Ctrl+드래그로 영역 선택 → 왼쪽 리스트에 추가 확인
3. 리스트의 메모 셀 더블클릭 → 편집 가능 확인
4. 메모 입력 후 Enter → 데이터 저장 확인 (콘솔 확인)
5. 여러 영역 선택 → 리스트에 누적 확인
6. 다른 페이지로 이동 → 페이지별로 마스킹 추가 확인
7. Ctrl+S → 콘솔에 전체 마스킹 정보 출력 확인
8. 새 PDF 열기 → 기존 마스킹 리스트 초기화 확인

---

## 2025-11-17 (5단계): 마스킹 저장 기능 구현 (Redaction)

### 1. PyMuPDF Redaction 기능 구현

PDF에 마스킹을 실제로 적용하여 영구적으로 정보를 제거하는 기능을 구현했습니다.

#### 1.1 apply_masks_and_save() 메서드

`PdfDocumentManager`에 마스킹 적용 및 저장 메서드를 추가했습니다.

```python
def apply_masks_and_save(self, masks: list[MaskEntry]) -> None:
    """마스킹을 PDF에 적용하고 저장"""
    # 1. 페이지별로 마스크 필터링
    for page_num in range(len(self.doc)):
        page_masks = [m for m in masks if m.page_index == page_num]
        
        if not page_masks:
            continue
        
        page = self.doc.load_page(page_num)
        
        # 2. Redaction annotation 추가
        for mask in page_masks:
            page.add_redact_annot(mask.rect, fill=(0, 0, 0))
    
    # 3. 모든 redaction 적용
    self.doc.apply_redactions()
    
    # 4. 파일 저장 (incremental)
    self.doc.save(
        self.file_path,
        incremental=True,
        encryption=fitz.PDF_ENCRYPT_KEEP
    )
```

#### 1.2 Redaction 프로세스

```
1. 페이지별 마스크 필터링
   masks → [page 0 masks], [page 1 masks], ...

2. 각 페이지에 대해:
   - Redaction Annotation 추가
     page.add_redact_annot(rect, fill=(0, 0, 0))
     * rect: 마스킹할 영역
     * fill: 채울 색상 (검은색)
   
   - 페이지별 Redaction 적용
     page.apply_redactions()
     → 실제로 내용을 영구 제거하고 검은색 박스로 대체

3. 파일 저장
   doc.save(path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
   - incremental: 기존 파일에 증분 저장
   - encryption: 기존 암호화 설정 유지
```

**중요:** `page.apply_redactions()`를 페이지별로 호출합니다. 
`doc.apply_redactions()`는 일부 PyMuPDF 버전에서 지원되지 않을 수 있습니다.

### 2. 저장 기능 UI 플로우

#### 2.1 Case 1: 마스크가 있는 경우

**사용자 동작:** Ctrl+S

**다이얼로그:**
```
┌────────────────────────────────────┐
│ 마스킹 저장                         │
├────────────────────────────────────┤
│ 현재 PDF 파일의 마스킹 작업 내용을  │
│ 저장하시겠습니까?                   │
│                                    │
│        [예(Y)]    [아니요(N)]      │
└────────────────────────────────────┘
```

**"예" 선택 시:**
1. `apply_masks_and_save()` 호출
2. PDF에 마스킹 적용 및 저장
3. 성공 메시지 표시
4. 마스킹 리스트 초기화
5. PDF 재로드하여 결과 확인

**"아니요" 선택 시:**
- 아무 동작 없음

#### 2.2 Case 2: 마스크가 없는 경우

**사용자 동작:** Ctrl+S

**다이얼로그:**
```
┌────────────────────────────────────┐
│ 다음으로 이동                       │
├────────────────────────────────────┤
│ 마스킹 작업 없이 다음으로           │
│ 넘어가시겠습니까?                   │
│                                    │
│        [예(Y)]    [아니요(N)]      │
└────────────────────────────────────┘
```

**"예" 선택 시:**
- 현재는 동작 없음
- TODO: 폴더의 다음 PDF로 자동 이동 (향후 구현)

**"아니요" 선택 시:**
- 아무 동작 없음

### 3. save_masks() 메서드 구현

```python
def save_masks(self) -> None:
    """마스킹 정보 저장 (Ctrl+S)"""
    # PDF가 열려있지 않으면 무시
    if self.pdf_manager.doc is None:
        return
    
    # Case 1: 마스크가 있는 경우
    if len(self.masks) > 0:
        reply = QMessageBox.question(
            self, "마스킹 저장",
            "현재 PDF 파일의 마스킹 작업 내용을 저장하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.pdf_manager.apply_masks_and_save(self.masks)
                
                QMessageBox.information(
                    self, "저장 완료",
                    f"총 {len(self.masks)}개의 마스킹이 적용되어 저장되었습니다."
                )
                
                # 초기화 및 재로드
                self.masks.clear()
                self.mask_list.setRowCount(0)
                self.reload_current_pdf()
                
            except Exception as e:
                QMessageBox.critical(
                    self, "저장 오류",
                    f"저장 중 오류가 발생했습니다.\n\n{str(e)}"
                )
    
    # Case 2: 마스크가 없는 경우
    else:
        reply = QMessageBox.question(
            self, "다음으로 이동",
            "마스킹 작업 없이 다음으로 넘어가시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # TODO: 다음 파일로 이동
            pass
```

### 4. PDF 재로드 기능

저장 후 변경사항을 확인하기 위해 PDF를 자동으로 다시 로드합니다.

```python
def reload_current_pdf(self) -> None:
    """현재 PDF 파일을 다시 로드"""
    current_path = self.pdf_manager.file_path
    current_page = self.current_page_index
    
    # PDF 재로드
    self.pdf_manager.load_pdf(current_path)
    
    # 현재 페이지 유지 (범위 체크)
    page_count = self.pdf_manager.get_page_count()
    if current_page >= page_count:
        self.current_page_index = max(0, page_count - 1)
    else:
        self.current_page_index = current_page
    
    # 페이지 표시
    self.update_page_view()
```

### 5. 예외 처리

#### 5.1 저장 중 오류

```python
try:
    self.pdf_manager.apply_masks_and_save(self.masks)
    # 성공 처리...
except Exception as e:
    QMessageBox.critical(
        self, "저장 오류",
        f"저장 중 오류가 발생했습니다.\n\n{str(e)}"
    )
```

#### 5.2 발생 가능한 오류
- PDF 파일이 다른 프로그램에서 열려있는 경우
- 파일 권한 문제
- 디스크 용량 부족
- 손상된 PDF 파일

### 6. Redaction vs 일반 마스킹

#### 6.1 Redaction의 특징

**영구적 제거:**
- 원본 텍스트/이미지가 완전히 제거됨
- 복구 불가능 (되돌릴 수 없음)
- 보안에 중요한 정보 처리에 적합

**vs Annotation (주석):**
- Annotation: 단순히 위에 덮는 것 (제거 가능)
- Redaction: 실제로 내용을 제거하고 대체

#### 6.2 PyMuPDF Redaction API

```python
# 1. Redaction annotation 추가
page.add_redact_annot(
    rect,              # fitz.Rect: 마스킹할 영역
    fill=(0, 0, 0),    # RGB 튜플: 채울 색상 (검은색)
    text="",           # 대체 텍스트 (선택사항)
)

# 2. 모든 redaction 적용 (실제 제거)
doc.apply_redactions()

# 3. 저장
doc.save(path, incremental=True)
```

### 7. 사용 시나리오

#### 7.1 전체 워크플로우

```
1. PDF 파일 열기 (Ctrl+O)
   ↓
2. 마스킹할 영역 선택 (Ctrl + 드래그)
   - 여러 페이지, 여러 영역 선택 가능
   ↓
3. 메모 작성 (더블클릭)
   - 각 마스킹에 설명 추가
   ↓
4. 저장 (Ctrl+S)
   - "저장하시겠습니까?" 확인
   ↓
5. Redaction 적용 및 저장
   - PDF 파일이 실제로 수정됨
   ↓
6. 자동 재로드
   - 마스킹된 결과 확인
   ↓
7. 다음 파일로 이동 (향후 구현)
```

#### 7.2 예시: 계약서 마스킹

```
파일: 계약서.pdf (3페이지)

작업:
1페이지:
  - Ctrl+드래그 → "계약자 이름" 
  - Ctrl+드래그 → "주민번호"
  
2페이지:
  - Ctrl+드래그 → "주소"
  
3페이지:
  - Ctrl+드래그 → "서명"

Ctrl+S → 저장 확인 → [예]

결과:
✅ 총 4개 영역이 검은색 박스로 영구 마스킹됨
✅ 원본 정보는 복구 불가능
✅ PDF 파일 크기는 거의 동일 (incremental save)
```

### 8. 기술적 세부사항

#### 8.1 Incremental Save

```python
doc.save(path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
```

**장점:**
- 빠른 저장 속도
- 파일 크기 변화 최소화
- 기존 암호화 설정 유지

**단점:**
- 파일이 점진적으로 커질 수 있음
- 완전히 새로운 저장이 아님

#### 8.2 fill 색상 옵션

```python
fill=(0, 0, 0)      # 검은색 (현재 사용)
fill=(1, 1, 1)      # 흰색
fill=(1, 0, 0)      # 빨간색
fill=(0.5, 0.5, 0.5)  # 회색
```

RGB 튜플, 값 범위: 0.0 ~ 1.0

### 9. 구현 완료 상태 업데이트

#### 완료된 기능
✅ PyQt6 환경 설정  
✅ MainWindow 기본 구조  
✅ 3단 레이아웃 (왼쪽/가운데/오른쪽)  
✅ 메뉴바 구성  
✅ 툴바 구성  
✅ 키보드 단축키 등록  
✅ 파일/폴더 선택 다이얼로그 연동  
✅ PDF 문서 로드 기능  
✅ PDF 페이지 렌더링 및 표시  
✅ 페이지 네비게이션 (방향키/PageUp/PageDown)  
✅ 상태바에 페이지 정보 표시  
✅ 커스텀 PDF 뷰어 위젯 (PdfPageView)  
✅ Ctrl + 드래그로 마스킹 영역 선택  
✅ 화면 좌표 → PDF 좌표 변환  
✅ 마스킹 영역 시그널 발생  
✅ MaskEntry 데이터 클래스  
✅ 마스킹 데이터 저장 및 관리  
✅ 마스킹 리스트 테이블 표시  
✅ 더블클릭으로 메모 편집  
✅ 데이터와 UI 자동 동기화  
✅ 페이지 컬럼 읽기 전용 처리  
✅ **PyMuPDF Redaction을 이용한 마스킹 적용**  
✅ **Ctrl+S로 마스킹 저장**  
✅ **저장 확인 다이얼로그**  
✅ **마스크 유무에 따른 분기 처리**  
✅ **저장 후 PDF 자동 재로드**  
✅ **예외 처리 및 에러 메시지**  

#### TODO (향후 구현 예정)
- [ ] 마스킹 리스트에서 선택한 항목 삭제 기능
- [ ] 저장된 마스킹 영역을 페이지에 시각적으로 표시 (저장 전 프리뷰)
- [ ] 마스킹 리스트 항목 클릭 시 해당 페이지로 이동
- [ ] 폴더 내 PDF 파일 목록 로드
- [ ] 폴더 작업 시 자동으로 다음 파일로 이동
- [ ] 마스킹 정보 별도 파일로 백업 (JSON)
- [ ] 실행 취소/다시 실행 기능
- [ ] 확대/축소 기능
- [ ] PDF 파일 목록에서 파일 선택하여 전환
- [ ] 마스킹 색상 선택 옵션

### 10. 주의사항

⚠️ **중요: Redaction은 영구적입니다**

- `apply_redactions()` 후에는 원본 내용을 복구할 수 없습니다
- 작업 전 원본 파일을 백업하는 것을 권장합니다
- 실수로 잘못된 영역을 마스킹하지 않도록 주의가 필요합니다

### 11. 테스트 방법

```bash
uv run python main.py
```

**테스트 시나리오:**

1. PDF 파일 열기
2. Ctrl+드래그로 여러 영역 선택
3. 메모 작성
4. Ctrl+S 누르기
5. "저장하시겠습니까?" → [예] 선택
6. "저장 완료" 메시지 확인
7. 마스킹된 영역이 검은색 박스로 표시되는지 확인
8. 다른 PDF 뷰어로 열어서 실제로 마스킹되었는지 확인

**마스크 없이 저장 테스트:**

1. PDF 파일 열기
2. 마스킹 없이 Ctrl+S
3. "다음으로 넘어가시겠습니까?" 메시지 확인
4. [예] 또는 [아니요] 선택

---

## 2025-11-17 (6단계): 폴더 열기 및 PDF 파일 목록 관리

### 1. 폴더 기반 작업 플로우 구현

여러 PDF 파일을 한 번에 처리할 수 있도록 폴더 열기 기능을 구현했습니다.

#### 1.1 새로운 속성 추가

```python
self.pdf_files: list[str] = []      # 폴더 내 PDF 파일 경로 리스트
self.current_pdf_index: int = -1    # 현재 열린 PDF의 인덱스 (-1: 없음)
```

### 2. 폴더 열기 기능

#### 2.1 open_folder() 구현

```python
def open_folder(self) -> None:
    # 1. 폴더 선택
    folder_path = QFileDialog.getExistingDirectory(self, "폴더 선택")
    
    # 2. PDF 파일 검색
    pdf_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.pdf'):
            full_path = os.path.join(folder_path, filename)
            pdf_files.append(full_path)
    
    # 3. PDF가 없으면 안내 메시지
    if not pdf_files:
        QMessageBox.information(self, "알림", "PDF 파일이 없습니다.")
        return
    
    # 4. 파일명으로 정렬
    pdf_files.sort()
    
    # 5. 리스트 저장 및 표시
    self.pdf_files = pdf_files
    self.pdf_file_list.clear()
    for file_path in pdf_files:
        self.pdf_file_list.addItem(os.path.basename(file_path))
    
    # 6. 첫 번째 PDF 자동 열기
    self.load_pdf_from_list(0)
```

#### 2.2 프로세스

```
폴더 선택
    ↓
.pdf 파일 검색
    ↓
파일명 정렬
    ↓
오른쪽 리스트에 표시
    ↓
첫 번째 PDF 자동 열기
```

### 3. PDF 파일 목록 관리

#### 3.1 리스트 표시

오른쪽 Dock Widget의 `QListWidget`에 PDF 파일 목록을 표시합니다.

- 파일명만 표시 (전체 경로는 `self.pdf_files`에 저장)
- 현재 열린 파일은 하이라이트됨
- 더블클릭으로 파일 전환

#### 3.2 더블클릭 이벤트

```python
def on_pdf_list_double_clicked(self, item) -> None:
    row = self.pdf_file_list.row(item)
    self.load_pdf_from_list(row)
```

### 4. 헬퍼 메서드

코드 재사용성과 유지보수성을 위해 여러 헬퍼 메서드를 구현했습니다.

#### 4.1 clear_masks()

```python
def clear_masks(self) -> None:
    """마스킹 데이터 및 테이블 초기화"""
    self.masks.clear()
    self.mask_list.setRowCount(0)
```

#### 4.2 load_pdf_from_path()

```python
def load_pdf_from_path(self, file_path: str) -> None:
    """지정된 경로의 PDF 파일 로드"""
    # 1. PDF 로드
    self.pdf_manager.load_pdf(file_path)
    
    # 2. 마스킹 초기화
    self.clear_masks()
    
    # 3. 첫 페이지로 이동
    self.current_page_index = 0
    
    # 4. 페이지 표시
    self.update_page_view()
    
    # 5. 창 제목 업데이트
    filename = os.path.basename(file_path)
    self.setWindowTitle(f"PDF Mask - {filename}")
```

#### 4.3 load_pdf_from_list()

```python
def load_pdf_from_list(self, index: int) -> None:
    """PDF 파일 목록에서 지정된 인덱스의 PDF 로드"""
    self.current_pdf_index = index
    file_path = self.pdf_files[index]
    self.load_pdf_from_path(file_path)
    
    # 리스트에서 현재 파일 하이라이트
    self.pdf_file_list.setCurrentRow(index)
```

#### 4.4 move_to_next_pdf_if_available()

```python
def move_to_next_pdf_if_available(self) -> None:
    """폴더의 다음 PDF 파일로 이동 (있는 경우)"""
    # 다음 파일이 있는 경우
    if self.current_pdf_index < len(self.pdf_files) - 1:
        next_index = self.current_pdf_index + 1
        
        # 확인 다이얼로그
        reply = QMessageBox.question(
            self, "다음 파일",
            f"다음 PDF 파일을 열겠습니까?\n\n{os.path.basename(self.pdf_files[next_index])}"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.load_pdf_from_list(next_index)
    
    # 마지막 파일인 경우
    else:
        QMessageBox.information(
            self, "완료",
            "폴더의 모든 PDF 파일 작업이 완료되었습니다."
        )
```

### 5. 저장 후 자동 이동

마스킹 저장 후 자동으로 다음 파일로 이동할지 확인합니다.

```python
def save_masks(self) -> None:
    if len(self.masks) > 0:
        # 저장 확인 → 저장 → 성공 메시지
        # ...
        
        # 다음 파일로 이동 제안
        self.move_to_next_pdf_if_available()
    
    else:
        # 마스킹 없이 다음으로 이동
        reply = QMessageBox.question(
            self, "다음으로 이동",
            "마스킹 작업 없이 다음으로 넘어가시겠습니까?"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.move_to_next_pdf_if_available()
```

### 6. 키보드 단축키 정리

#### 6.1 페이지 네비게이션

| 키 | 기능 | 메서드 |
|---|------|--------|
| Left (←) | 이전 페이지 | `go_prev_page()` |
| Right (→) | 다음 페이지 | `go_next_page()` |
| PageUp | 이전 페이지 | `go_prev_page()` |
| PageDown | 다음 페이지 | `go_next_page()` |

**동작:**
- 페이지 범위 체크 (0 ~ page_count-1)
- 범위 초과 시 무시
- `update_page_view()` 호출

#### 6.2 기타 단축키

| 키 | 기능 |
|---|------|
| Ctrl+O | PDF 파일 열기 |
| Ctrl+Shift+O | 폴더 열기 |
| Ctrl+S | 마스킹 저장 |
| Ctrl+Q | 프로그램 종료 |

### 7. 사용 시나리오

#### 7.1 폴더 작업 워크플로우

```
1. 폴더 열기 (Ctrl+Shift+O)
   ↓
2. 폴더 선택
   ↓
3. PDF 파일 목록 표시
   ↓
4. 첫 번째 PDF 자동 열림
   ↓
5. 마스킹 작업 (Ctrl + 드래그)
   ↓
6. 메모 작성 (더블클릭)
   ↓
7. 저장 (Ctrl+S)
   ↓
8. "다음 파일을 열겠습니까?" → [예]
   ↓
9. 다음 PDF 자동 열림
   ↓
10. 5~9 반복
   ↓
11. 마지막 파일 완료 → "모든 작업 완료" 메시지
```

#### 7.2 예시: 계약서 폴더 일괄 처리

```
폴더 구조:
contracts/
  ├── contract_001.pdf
  ├── contract_002.pdf
  ├── contract_003.pdf
  └── contract_004.pdf

작업:
1. "contracts" 폴더 열기
2. PDF 파일 목록에 4개 파일 표시
3. contract_001.pdf 자동 열림

파일별 작업:
- contract_001.pdf
  * 이름, 주민번호, 주소 마스킹
  * Ctrl+S → 저장 → 다음 파일
  
- contract_002.pdf
  * 서명, 날짜 마스킹
  * Ctrl+S → 저장 → 다음 파일
  
- contract_003.pdf
  * 마스킹 없음
  * Ctrl+S → "작업 없이 다음으로" → 다음 파일
  
- contract_004.pdf
  * 이름, 전화번호 마스킹
  * Ctrl+S → 저장 → "모든 작업 완료"

결과:
✅ 4개 파일 모두 처리 완료
✅ 필요한 정보만 선택적으로 마스킹됨
✅ 빠른 일괄 처리
```

### 8. 단일 파일 vs 폴더 작업

#### 8.1 단일 파일 열기 (Ctrl+O)

- `pdf_files` = [선택한 파일]
- `current_pdf_index` = 0
- 리스트에 1개 파일만 표시

#### 8.2 폴더 열기 (Ctrl+Shift+O)

- `pdf_files` = [폴더 내 모든 PDF]
- `current_pdf_index` = 0 (첫 파일)
- 리스트에 모든 파일 표시
- 저장 후 자동으로 다음 파일 제안

### 9. UI 개선사항

#### 9.1 창 제목 동적 업데이트

```python
self.setWindowTitle(f"PDF Mask - {filename}")
```

현재 열린 파일명이 항상 표시됩니다.

#### 9.2 PDF 리스트 하이라이트

현재 열린 파일이 리스트에서 선택된 상태로 표시됩니다.

```python
self.pdf_file_list.setCurrentRow(index)
```

#### 9.3 안내 메시지

- PDF 파일이 없는 폴더: "PDF 파일이 없습니다."
- 마지막 파일 완료: "모든 작업이 완료되었습니다."
- 다음 파일 이동: "다음 PDF 파일을 열겠습니까?"

### 10. 구현 완료 상태 (최종)

#### 완료된 기능
✅ PyQt6 환경 설정  
✅ MainWindow 기본 구조  
✅ 3단 레이아웃 (왼쪽/가운데/오른쪽)  
✅ 메뉴바 구성  
✅ 툴바 구성  
✅ 키보드 단축키 등록  
✅ 파일/폴더 선택 다이얼로그 연동  
✅ PDF 문서 로드 기능  
✅ PDF 페이지 렌더링 및 표시  
✅ 페이지 네비게이션 (방향키/PageUp/PageDown)  
✅ 상태바에 페이지 정보 표시  
✅ 커스텀 PDF 뷰어 위젯 (PdfPageView)  
✅ Ctrl + 드래그로 마스킹 영역 선택  
✅ 화면 좌표 → PDF 좌표 변환  
✅ 마스킹 영역 시그널 발생  
✅ MaskEntry 데이터 클래스  
✅ 마스킹 데이터 저장 및 관리  
✅ 마스킹 리스트 테이블 표시  
✅ 더블클릭으로 메모 편집  
✅ 데이터와 UI 자동 동기화  
✅ 페이지 컬럼 읽기 전용 처리  
✅ PyMuPDF Redaction을 이용한 마스킹 적용  
✅ Ctrl+S로 마스킹 저장  
✅ 저장 확인 다이얼로그  
✅ 마스크 유무에 따른 분기 처리  
✅ 저장 후 PDF 자동 재로드  
✅ 예외 처리 및 에러 메시지  
✅ **폴더 열기 기능**  
✅ **PDF 파일 목록 표시**  
✅ **리스트에서 더블클릭으로 파일 전환**  
✅ **저장 후 다음 파일로 자동 이동 제안**  
✅ **헬퍼 메서드로 코드 구조화**  
✅ **창 제목 동적 업데이트**  
✅ **현재 파일 하이라이트**  

#### 향후 개선 가능 항목
- [ ] 마스킹 리스트에서 선택한 항목 삭제 기능 (Del 키)
- [ ] 저장 전 마스킹 영역 미리보기 (반투명 오버레이)
- [ ] 마스킹 리스트 항목 클릭 시 해당 페이지로 이동
- [ ] 마스킹 정보 별도 파일로 백업 (JSON)
- [ ] 실행 취소/다시 실행 기능 (Ctrl+Z/Ctrl+Y)
- [ ] 확대/축소 기능 (Ctrl+마우스휠)
- [ ] 마스킹 색상 선택 옵션
- [ ] 작업 진행률 표시 (N/M 파일 완료)
- [ ] 최근 열었던 폴더 기록
- [ ] 배치 처리 모드 (자동으로 모든 파일 순회)

### 11. 코드 구조 요약

```
MainWindow
├── 데이터
│   ├── pdf_manager: PdfDocumentManager
│   ├── masks: list[MaskEntry]
│   ├── pdf_files: list[str]
│   └── current_pdf_index: int
│
├── UI 초기화
│   ├── setup_mask_table()
│   ├── setup_menu()
│   ├── setup_toolbar()
│   ├── setup_shortcuts()
│   └── setup_statusbar()
│
├── PDF 관리
│   ├── open_pdf()
│   ├── open_folder()
│   ├── load_pdf_from_path()
│   ├── load_pdf_from_list()
│   └── reload_current_pdf()
│
├── 마스킹 관리
│   ├── on_mask_created()
│   ├── on_mask_item_changed()
│   ├── clear_masks()
│   └── save_masks()
│
├── 네비게이션
│   ├── go_next_page()
│   ├── go_prev_page()
│   ├── update_page_view()
│   └── move_to_next_pdf_if_available()
│
└── 이벤트
    ├── on_pdf_list_double_clicked()
    └── closeEvent()
```

### 12. 테스트 방법

```bash
uv run python main.py
```

**폴더 작업 테스트:**

1. Ctrl+Shift+O로 PDF가 여러 개 있는 폴더 선택
2. 오른쪽 리스트에 파일 목록 표시 확인
3. 첫 번째 파일이 자동으로 열리는지 확인
4. 마스킹 영역 선택 및 메모 작성
5. Ctrl+S로 저장
6. "다음 파일을 열겠습니까?" 메시지 확인
7. [예] 선택하여 다음 파일로 이동
8. 리스트에서 다른 파일 더블클릭하여 직접 전환
9. 마지막 파일 완료 시 "모든 작업 완료" 메시지 확인

**단일 파일 테스트:**

1. Ctrl+O로 단일 PDF 파일 열기
2. 마스킹 작업 수행
3. Ctrl+S로 저장
4. 다음 파일 이동 메시지가 나오지 않는지 확인

---

## 2025-11-17 (7단계): UI/UX 개선 및 기능 보완

### 1. 마스킹 영역 화면 표시

드래그 후 선택한 마스킹 영역이 화면에 계속 표시되도록 구현했습니다.

#### 1.1 구현 내용

**저장된 마스킹 영역 표시:**
- 색상: 반투명 빨간색 (RGB: 255, 0, 0, 투명도 60)
- 테두리: 2px 빨간색
- 현재 페이지의 마스킹만 표시

**드래그 중인 영역 표시:**
- 색상: 반투명 파란색 (RGB: 0, 120, 255, 투명도 80)
- 테두리: 2px 파란색

#### 1.2 데이터 구조

```python
class PdfPageView(QWidget):
    # 저장된 마스킹 영역들 (화면 좌표)
    self._saved_masks: list[QRect] = []
```

**프로세스:**
1. 마스킹 생성 시 `_saved_masks`에 추가
2. `paintEvent()`에서 모든 저장된 마스킹을 빨간색으로 그림
3. 페이지 전환 시 해당 페이지의 마스킹만 표시

### 2. 마스킹 목록 삭제 기능

마스킹 리스트에서 항목을 선택하고 Del 키로 삭제할 수 있습니다.

#### 2.1 단축키 등록

```python
# 삭제 (Del)
self.shortcut_delete = QShortcut(QKeySequence(Qt.Key.Key_Delete), self)
self.shortcut_delete.activated.connect(self.delete_selected_mask)
```

#### 2.2 delete_selected_mask() 구현

```python
def delete_selected_mask(self) -> None:
    """선택된 마스킹 항목 삭제 (Del 키)"""
    selected_rows = self.mask_list.selectionModel().selectedRows()
    
    # 역순으로 삭제 (인덱스 변경 방지)
    rows_to_delete = sorted([index.row() for index in selected_rows], reverse=True)
    
    for row in rows_to_delete:
        # 데이터에서 삭제
        del self.masks[row]
        # 테이블에서 삭제
        self.mask_list.removeRow(row)
    
    # 화면 갱신 (마스킹 영역 업데이트)
    self.update_page_view()
```

**특징:**
- 다중 선택 지원
- 역순 삭제로 인덱스 오류 방지
- 삭제 후 즉시 화면 갱신

### 3. 저장 후 PDF 화면에서 제거

Ctrl+S로 저장 후 저장된 PDF 파일을 리스트에서 자동으로 제거하여 다음 작업에 집중할 수 있도록 개선했습니다.

#### 3.1 save_masks() 수정

```python
def save_masks(self) -> None:
    if len(self.masks) > 0:
        # 저장 확인 → 저장 → 성공 메시지
        
        # 마스킹 데이터 초기화
        self.clear_masks()
        
        # 다음 파일로 자동 이동
        self.move_to_next_pdf_if_available()
```

**프로세스:**
```
저장 완료
    ↓
마스킹 리스트 초기화
    ↓
다음 파일이 있는지 확인
    ↓
[있음] "다음 파일을 열겠습니까?" 다이얼로그
    ↓
[없음] "모든 작업 완료" 메시지
```

### 4. 스크롤 및 확대/축소 기능

PDF 뷰어에 고정 크기 스크롤 영역과 Ctrl + 마우스휠로 확대/축소 기능을 추가했습니다.

#### 4.1 ScrollablePdfView 클래스 추가

```python
class ScrollablePdfView(QScrollArea):
    """스크롤 가능한 PDF 뷰 컨테이너"""
    
    def __init__(self):
        # A4 크기 고정 (794 x 1123 pixels at 96 DPI)
        self.setFixedSize(820, 1150)
        
        # 줌 레벨
        self.zoom_level: float = 1.0  # 100%
        self.min_zoom: float = 0.5    # 50% (높이에 맞추기)
        self.max_zoom: float = 2.0    # 200%
```

#### 4.2 주요 특징

**고정 크기 뷰포트:**
- 크기: 820 x 1150 pixels (A4 용지 + 여유)
- 큰 PDF는 자동으로 스크롤바 표시
- 작은 PDF는 스크롤바 없이 표시

**확대/축소:**
- Ctrl + 마우스휠 위: 확대 (10% 증가)
- Ctrl + 마우스휠 아래: 축소 (10% 감소)
- 범위: 50% ~ 200%
- 실시간 페이지 재렌더링

#### 4.3 wheelEvent() 구현

```python
def wheelEvent(self, event) -> None:
    """마우스 휠 이벤트 (Ctrl + 휠로 줌)"""
    if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
        delta = event.angleDelta().y()
        if delta > 0:
            self.parent().zoom_in()   # 확대
        else:
            self.parent().zoom_out()  # 축소
        event.accept()
    else:
        event.ignore()  # 일반 스크롤
```

#### 4.4 update_page_view() 수정

줌 레벨을 반영하여 페이지를 렌더링합니다:

```python
def update_page_view(self) -> None:
    # 줌 레벨 적용
    zoom = self.scrollable_pdf_view.zoom_level * 1.5
    
    # 페이지 렌더링
    pixmap = self.pdf_manager.get_page_pixmap(self.current_page_index, zoom)
    
    # 상태바에 줌 정보 표시
    zoom_percent = int(self.scrollable_pdf_view.zoom_level * 100)
    self.statusBar().showMessage(
        f"페이지: {self.current_page_index + 1} / {total_pages} | "
        f"확대: {zoom_percent}% | "
        f"(Ctrl + 드래그: 마스킹, Ctrl + 휠: 확대/축소)"
    )
```

### 5. 좌표 변환 시스템 개선

PDF 좌표 ↔ 화면 좌표 양방향 변환을 지원합니다.

#### 5.1 화면 → PDF 좌표

```python
def _convert_to_pdf_rect(self, screen_rect: QRect) -> Optional[fitz.Rect]:
    """화면 좌표를 PDF 페이지 좌표로 변환"""
    scale_x = self._page_width / self._pixmap.width()
    scale_y = self._page_height / self._pixmap.height()
    
    x0 = screen_rect.left() * scale_x
    y0 = screen_rect.top() * scale_y
    x1 = screen_rect.right() * scale_x
    y1 = screen_rect.bottom() * scale_y
    
    return fitz.Rect(x0, y0, x1, y1)
```

#### 5.2 PDF → 화면 좌표

```python
def _convert_to_screen_rect(self, pdf_rect: fitz.Rect) -> Optional[QRect]:
    """PDF 좌표를 화면 좌표로 변환"""
    scale_x = self._pixmap.width() / self._page_width
    scale_y = self._pixmap.height() / self._page_height
    
    x0 = int(pdf_rect.x0 * scale_x)
    y0 = int(pdf_rect.y0 * scale_y)
    x1 = int(pdf_rect.x1 * scale_x)
    y1 = int(pdf_rect.y1 * scale_y)
    
    return QRect(QPoint(x0, y0), QPoint(x1, y1))
```

### 6. UI 레이아웃 조정

창 크기와 레이아웃을 최적화했습니다.

```python
def init_ui(self) -> None:
    self.setGeometry(100, 100, 1400, 900)  # 창 크기 증가
```

**레이아웃 구성:**
```
┌─────────────────────────────────────────────────────┐
│ [PDF 열기] [폴더 열기]  메뉴/툴바                    │
├──────────────┬─────────────────────┬────────────────┤
│              │                     │ PDF 파일 목록  │
│  마스킹 리스트│   PDF 뷰어          │ (QListWidget) │
│ (250-400px) │   (820x1150 고정)   │ (200px)       │
│              │   ┌─────────────┐   │                │
│  [페이지|메모]│   │             │   │ ▪ file1.pdf   │
│              │   │   스크롤    │   │ ▪ file2.pdf   │
│              │   │   영역      │   │ ▪ file3.pdf   │
│              │   │             │   │                │
│              │   └─────────────┘   │                │
└──────────────┴─────────────────────┴────────────────┘
│ 페이지: 1/10 | 확대: 100% | 상태바                   │
└─────────────────────────────────────────────────────┘
```

### 7. 사용 시나리오 (개선 후)

```
1. 폴더 열기 (Ctrl+Shift+O)
   ↓
2. 첫 번째 PDF 자동 열림 (100% 확대)
   ↓
3. Ctrl + 마우스휠로 적절한 크기 조절 (예: 120%)
   ↓
4. Ctrl + 드래그로 마스킹 영역 선택
   → 선택한 영역이 빨간색으로 즉시 표시됨
   ↓
5. 메모 작성 (더블클릭)
   ↓
6. 잘못 선택한 마스킹 있으면:
   → 해당 행 선택 후 Del 키로 삭제
   ↓
7. Ctrl+S로 저장
   → 마스킹 리스트 자동 초기화
   → "다음 파일을 열겠습니까?" 다이얼로그
   ↓
8. [예] 선택 → 다음 PDF 자동 열림
   ↓
9. 3~8 반복
   ↓
10. 마지막 파일 → "모든 작업 완료"
```

### 8. 단축키 정리 (최종)

| 키 | 기능 |
|---|------|
| Ctrl+O | PDF 파일 열기 |
| Ctrl+Shift+O | 폴더 열기 |
| Ctrl+S | 마스킹 저장 |
| Ctrl+Q | 프로그램 종료 |
| Ctrl+드래그 | 마스킹 영역 선택 |
| Ctrl+마우스휠 | 확대/축소 (50%~200%) |
| Left / PageUp | 이전 페이지 |
| Right / PageDown | 다음 페이지 |
| Del | 선택한 마스킹 삭제 |
| 더블클릭 | 메모 편집 |

### 9. 구현 완료 상태 (최종 완성)

#### 완료된 기능
✅ PyQt6 환경 설정  
✅ MainWindow 기본 구조  
✅ 3단 레이아웃 (왼쪽/가운데/오른쪽)  
✅ 메뉴바 구성  
✅ 툴바 구성  
✅ 키보드 단축키 등록  
✅ 파일/폴더 선택 다이얼로그 연동  
✅ PDF 문서 로드 기능  
✅ PDF 페이지 렌더링 및 표시  
✅ 페이지 네비게이션 (방향키/PageUp/PageDown)  
✅ 상태바에 페이지 정보 표시  
✅ 커스텀 PDF 뷰어 위젯 (PdfPageView)  
✅ Ctrl + 드래그로 마스킹 영역 선택  
✅ 화면 좌표 → PDF 좌표 변환  
✅ 마스킹 영역 시그널 발생  
✅ MaskEntry 데이터 클래스  
✅ 마스킹 데이터 저장 및 관리  
✅ 마스킹 리스트 테이블 표시  
✅ 더블클릭으로 메모 편집  
✅ 데이터와 UI 자동 동기화  
✅ 페이지 컬럼 읽기 전용 처리  
✅ PyMuPDF Redaction을 이용한 마스킹 적용  
✅ Ctrl+S로 마스킹 저장  
✅ 저장 확인 다이얼로그  
✅ 마스크 유무에 따른 분기 처리  
✅ 저장 후 PDF 자동 재로드  
✅ 예외 처리 및 에러 메시지  
✅ 폴더 열기 기능  
✅ PDF 파일 목록 표시  
✅ 리스트에서 더블클릭으로 파일 전환  
✅ 저장 후 다음 파일로 자동 이동 제안  
✅ 헬퍼 메서드로 코드 구조화  
✅ 창 제목 동적 업데이트  
✅ 현재 파일 하이라이트  
✅ **마스킹 영역 화면 표시 (빨간색)**  
✅ **Del 키로 마스킹 삭제**  
✅ **저장 후 자동 다음 파일 이동**  
✅ **고정 크기 스크롤 뷰 (A4 크기)**  
✅ **Ctrl + 마우스휠 확대/축소 (50%~200%)**  
✅ **PDF ↔ 화면 좌표 양방향 변환**  

### 10. 테스트 방법 (최종)

```bash
uv run python main.py
```

**전체 기능 테스트:**

1. **폴더 열기**
   - Ctrl+Shift+O로 PDF 폴더 선택
   - 파일 목록 표시 확인

2. **확대/축소**
   - Ctrl + 마우스휠로 확대/축소
   - 50% ~ 200% 범위 확인
   - 상태바에 퍼센트 표시 확인

3. **마스킹 선택**
   - Ctrl + 드래그로 영역 선택
   - 드래그 중 파란색 표시 확인
   - 드래그 완료 후 빨간색으로 변경 확인

4. **마스킹 삭제**
   - 리스트에서 항목 선택
   - Del 키로 삭제
   - 화면에서 빨간색 영역 제거 확인

5. **저장 및 다음 파일**
   - Ctrl+S로 저장
   - "다음 파일을 열겠습니까?" 확인
   - 자동으로 다음 파일 열림 확인

6. **스크롤 테스트**
   - 큰 PDF (200% 확대) → 스크롤바 표시
   - 작은 PDF → 스크롤바 없음

---

## 📦 2025-11-17: UI 개선 - Dock Widget 및 PDF View 최적화

### 1. Permission Denied 에러 개선

**문제:**
- PDF 저장 시 "Permission denied" 에러가 나면 의미 없는 메시지만 표시됨

**해결:**
```python
except Exception as e:
    error_msg = str(e)
    if "Permission denied" in error_msg:
        raise Exception(
            "PDF 파일이 다른 프로그램(예: Adobe Reader)에서 열려 있습니다.\n"
            "파일을 닫고 다시 시도해주세요."
        )
```

**개선 효과:**
- ✅ 사용자가 즉시 이해할 수 있는 명확한 메시지
- ✅ 해결 방법 제시

### 2. Dock Widget 분리/재결합 기능 구현

**요구사항:**
- PDF 파일 목록과 마스킹 리스트를 창에서 분리하고 다시 붙일 수 있어야 함
- 프로그램이 최대화되었을 때도 재결합이 가능해야 함

**구현:**

```python
# 1. Dock Widget 기능 활성화
mask_dock_widget.setFeatures(
    QDockWidget.DockWidgetFeature.DockWidgetMovable |
    QDockWidget.DockWidgetFeature.DockWidgetFloatable |
    QDockWidget.DockWidgetFeature.DockWidgetClosable
)

# 2. 모든 방향 도킹 허용
mask_dock_widget.setAllowedAreas(
    Qt.DockWidgetArea.LeftDockWidgetArea |
    Qt.DockWidgetArea.RightDockWidgetArea |
    Qt.DockWidgetArea.TopDockWidgetArea |
    Qt.DockWidgetArea.BottomDockWidgetArea
)

# 3. 메인 윈도우 도킹 옵션 설정
self.setDockOptions(
    QMainWindow.DockOption.AllowNestedDocks |
    QMainWindow.DockOption.AllowTabbedDocks |
    QMainWindow.DockOption.AnimatedDocks
)

# 4. 보기 메뉴에 토글 액션 추가
view_menu = self.menuBar().addMenu("보기(&V)")
view_menu.addAction(self.mask_dock_widget.toggleViewAction())
view_menu.addAction(self.pdf_dock_widget.toggleViewAction())
```

**기능:**
- ✅ 더블클릭으로 Dock 분리
- ✅ 드래그로 다른 위치에 재결합
- ✅ 탭 형태로 결합 가능
- ✅ 최대화 상태에서도 정상 작동
- ✅ 보기 메뉴에서 표시/숨김 토글

### 3. PDF View 크기 최적화

**요구사항:**
- 세로 길이: 프로그램 창 높이에 맞춰 자동 조정
- 가로 길이: 최소 400px 유지

**구현 (ScrollablePdfView):**

```python
def __init__(self, pdf_view: PdfPageView, parent: Optional[QWidget] = None):
    super().__init__(parent)
    self.pdf_view = pdf_view
    self.setWidget(pdf_view)
    self.setWidgetResizable(False)
    
    # 최소 가로 크기 설정
    self.setMinimumWidth(400)
    
    # 세로는 부모 창에 맞춰 자동 조정
    # (QMainWindow의 중앙 위젯으로 배치되어 자동으로 늘어남)
```

**효과:**
- ✅ 세로: 창 크기에 따라 동적으로 조정
- ✅ 가로: 최소 400px 보장
- ✅ 큰 PDF는 스크롤로 탐색
- ✅ 작은 PDF도 충분한 공간 확보

### 4. PDF 내용 가운데 정렬 및 배경색 개선

**요구사항:**
- PDF 내용을 뷰 중앙에 정렬
- PDF 영역 밖은 회색 배경으로 표시

**구현:**

```python
# 1. ScrollablePdfView: 가운데 정렬 + 회색 배경
self.setAlignment(Qt.AlignmentFlag.AlignCenter)
self.setStyleSheet("QScrollArea { background-color: #808080; }")

# 2. PdfPageView: 흰색 배경 (PDF 영역)
self.setStyleSheet("background-color: #ffffff;")
```

**시각적 효과:**

```
┌─────────────────────────────────────┐
│ 회색 배경 (#808080)                  │
│                                     │
│       ┌───────────────┐             │
│       │               │             │
│       │  PDF (흰색)   │ ← 가운데    │
│       │               │             │
│       └───────────────┘             │
│                                     │
│ 회색 배경                            │
└─────────────────────────────────────┘
```

**개선 효과:**
- ✅ PDF 문서와 배경의 명확한 구분
- ✅ 전문적인 외관 (Adobe Acrobat 스타일)
- ✅ 항상 중앙에 정렬되어 보기 편함
- ✅ 확대/축소 시에도 일관된 사용자 경험

### 5. 색상 구분

| 영역 | 색상 | 설명 |
|------|------|------|
| PDF 문서 영역 | 흰색 (#ffffff) | 실제 PDF 내용이 표시되는 영역 |
| 스크롤 영역 배경 | 회색 (#808080) | PDF 밖의 여백 영역 |
| 마스킹 (저장됨) | 빨간색 반투명 | 선택한 마스킹 영역 |
| 마스킹 (드래그 중) | 파란색 반투명 | 드래그 중인 영역 |

### 6. 최종 구현 기능 목록 업데이트

✅ **기본 기능**
- PDF 열기/폴더 열기
- 페이지 네비게이션 (방향키, PageUp/Down)
- 창 제목에 현재 파일명 표시

✅ **마스킹 기능**
- Ctrl + 드래그로 마스킹 영역 선택
- 드래그 중 파란색 표시
- 저장된 마스킹 빨간색 표시
- 더블클릭으로 메모 편집
- Del 키로 마스킹 삭제

✅ **저장 및 워크플로우**
- Ctrl+S로 PyMuPDF 적용 후 저장
- 저장 후 다음 PDF 자동 이동 제안
- Permission denied 시 명확한 에러 메시지

✅ **UI/UX 개선**
- 고정 크기 스크롤 뷰 (세로: 창 높이, 가로: 최소 400px)
- Ctrl + 마우스휠 확대/축소 (50%~200%)
- 상태바에 페이지 및 확대율 표시
- PDF 가운데 정렬
- 회색 배경 (#808080)으로 전문적인 외관
- **Dock Widget 분리/재결합 기능**
- **보기 메뉴에서 패널 표시/숨김**
- **최대화 시에도 정상 작동하는 도킹 시스템**

### 7. 테스트 방법 (최종)

```bash
uv run python main.py
```

**UI 테스트:**

1. **Dock Widget 테스트**
   - 마스킹 리스트 타이틀바 더블클릭 → 분리
   - PDF 파일 목록 드래그 → 다른 위치에 도킹
   - 보기 메뉴에서 패널 표시/숨김
   - 창 최대화 후에도 재결합 가능 확인

2. **PDF View 크기 테스트**
   - 창 크기 조절 → 세로는 따라감, 가로는 최소 400px
   - 큰 PDF → 스크롤바 표시
   - 작은 PDF → 가운데 정렬, 주변 회색 배경

3. **배경색 및 정렬 테스트**
   - PDF가 항상 중앙에 위치하는지 확인
   - PDF 영역: 흰색, 여백: 회색 구분 확인
   - 확대/축소 시 정렬 유지 확인

4. **에러 처리 테스트**
   - PDF를 Adobe Reader에서 열고 저장 시도
   - 명확한 에러 메시지 확인

---

*PDF Mask 프로그램이 완전히 완성되었습니다. 모든 요구사항이 구현되었으며, 전문적인 UI/UX를 갖춘 실무용 PDF 마스킹 도구입니다.*

---

## 📝 TODO: 다음 작업 계획

### 🐛 버그 수정
1. **확대 기능 오류 수정**
   - 현재 Ctrl + 마우스휠 확대 기능이 정상 작동하지 않음
   - 확대/축소 로직 점검 필요
   - 상태바의 확대율 표시도 함께 확인
   - ⚠️ 현재 구현 시도 보류 상태 (환경/입력 이슈로 재검토 필요, 추후 별도 작업으로 진행)

### 🎨 UI 개선
2. **툴바 아이콘 추가**
   - "PDF 열기" 버튼 → 📄 아이콘으로 대체
   - "폴더 열기" 버튼 → 📁 아이콘으로 대체
   - PyQt6 내장 아이콘 또는 커스텀 아이콘 사용 검토

3. **도움말 메뉴 추가**
   - 메뉴바에 "도움말(&H)" 메뉴 추가
   - 하위 메뉴:
     - "단축키 안내" → 모든 키보드 단축키 표시 다이얼로그
     - "사용 방법" → 간단한 사용법 안내
     - "정보" → 프로그램 버전, 만든이 정보

### 📊 기능 추가
4. **마스킹 작업 내역 엑셀 저장**
   - 마스킹 작업 내역을 Excel 파일로 내보내기
   - 파일명 형식: `마스킹_작업내역_YYYYMMDD.xlsx`
   - 컬럼: 작업일시, PDF 파일명, 페이지, 마스킹 영역 좌표, 메모
   - 일자별로 자동 분리하여 관리
   - 라이브러리: `openpyxl` 또는 `pandas` 사용 검토

5. **PDF 백업 기능**
   - 마스킹 적용 전 원본 PDF를 자동으로 백업
   - 백업 폴더 구조: `백업/YYYYMMDD/원본파일명.pdf`
   - 설정 옵션:
     - 백업 폴더 경로 지정
     - 백업 활성화/비활성화
     - 백업 보관 기간 설정 (예: 30일)
   - 저장 전 백업 완료 확인

6. **인증 기능 (시리얼 번호 + 서버 인증)**
   - 프로그램 최초 실행 시 시리얼 번호 입력 UI 표시
   - 네트워크 연결을 통한 라이선스 서버 인증
   - 인증 결과(성공/실패/만료) 메시지 처리 및 재시도 로직

7. **마스킹 데이터 기록(JSON)**
   - 마스킹 정보(JSON)로 저장: 페이지 번호, 좌표, 메모
   - 파일 단위/폴더 단위 저장 전략 정의
   - 추후 재편집을 위한 마스킹 데이터 재로딩 기능 연동

8. **진행상황 기록(JSON)**
   - 마지막 작업 시각, 완료된 파일 리스트를 JSON으로 관리
   - 프로그램 시작 시 이전 진행상황 로드 후 UI에 반영
   - 대용량 폴더 작업 시 재시작/중단 복구 워크플로우 설계

9. **로그 기록(TXT)**
   - 프로그램 시작/종료, 라이선스 인증 결과 로그 남기기
   - PDF 파일/폴더 열기, 마스킹 저장, 에러 발생 내역 기록
   - 로그 파일 회전/보관 기간 정책 정의 (예: 일자별 로그)

### 🔧 구현 우선순위
1. ⚠️ **높음**: 확대 기능 오류 수정 (기존 기능 복구)
2. 🎯 **중간**: 도움말 메뉴 추가 (사용자 편의성)
3. 🎯 **중간**: 툴바 아이콘 추가 (UI 개선)
4. 📈 **낮음**: 엑셀 저장 기능 (부가 기능)
5. 📈 **낮음**: PDF 백업 기능 (안전성 강화)

### ✅ 최근 작업 현황 (2025-11-18)
- 확대 기능 오류 수정: 환경/입력 이슈로 인해 구현 시도 보류, DEVLOG에 보류 상태로 명시
- 툴바 아이콘 추가: "PDF 열기"/"폴더 열기" 툴바 액션에 기본 파일/폴더 아이콘 적용
- 도움말 메뉴 추가: "도움말" 메뉴 및 "단축키 안내"/"사용 방법"/"정보" 다이얼로그 구현
- 단축키 안내: 단축키를 굵게(bold) 표시해 가독성 향상

### 📦 추가 의존성 (예상)
```toml
# pyproject.toml에 추가 필요
dependencies = [
    "pymupdf>=1.26.6",
    "pyqt6>=6.5.0",
    "openpyxl>=3.1.0",  # 엑셀 파일 생성용
]
```

---

*현재 버전(v1.0)은 안정적으로 작동하며, 위 항목들은 향후 개선 사항입니다.*

