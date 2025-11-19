# PDF Mask 개발 로그

## 프로젝트 개요
- **프로젝트명**: PDF Mask
- **버전**: v1.5.0
- **설명**: PDF 마스킹 프로그램 (개인정보 영구 제거)
- **Python 버전**: 3.12
- **주요 라이브러리**: PyQt6, PyMuPDF (fitz), openpyxl

---

## 개발 일정 요약

| 날짜 | 단계 | 주요 기능 |
|------|------|----------|
| 2025-11-17 | 1-4단계 | GUI 구조, PDF 렌더링, 마스킹 선택, 데이터 관리 |
| 2025-11-17 | 5-7단계 | Redaction 저장, 폴더 작업, UI/UX 개선 |
| 2025-11-18 | 8-9단계 | 백업, 인증, JSON 데이터, 진행상황, 로그 |
| 2025-11-19 | 리팩토링 | 프로젝트 모듈화, 문서화, 구조 개선 |

---

## 📋 구현 완료 기능 (v1.5.0)

### 기본 기능
- ✅ PyQt6 기반 3단 레이아웃 (마스킹 리스트 / PDF 뷰 / 파일 목록)
- ✅ PDF 문서 로드 및 페이지 렌더링
- ✅ 페이지 네비게이션 (방향키, PageUp/Down)
- ✅ 메뉴바 (파일, 보기, 설정, 도움말) 및 툴바
- ✅ Dock Widget 분리/재결합
- ✅ 단축키 시스템

### 마스킹 기능
- ✅ Ctrl + 드래그로 마스킹 영역 선택
- ✅ 실시간 미리보기 (드래그: 파란색, 저장: 빨간색)
- ✅ 더블클릭 메모 편집
- ✅ Del 키로 삭제
- ✅ PyMuPDF Redaction으로 영구 제거 (흰색)
- ✅ 화면 ↔ PDF 좌표 양방향 변환

### 파일 관리
- ✅ 단일 PDF / 폴더 일괄 처리
- ✅ 저장 후 다음 파일 자동 이동
- ✅ 완료 파일 체크마크 표시

### 데이터 관리 (v1.5 신규)
- ✅ **자동 백업**: `backup/YYYYMMDD/` 폴더에 원본 저장
- ✅ **라이선스 인증**: 시리얼 번호 기반 (테스트: TEST-1234-5678-ABCD)
- ✅ **마스킹 데이터**: 일자별 JSON (`mask_data_YYYYMMDD.json`)
- ✅ **진행 상황**: 폴더 작업 중단/복구 (`progress.json`)
- ✅ **로그 기록**: 일자별 로그 (`pdfmask_YYYYMMDD.log`)

### 프로젝트 구조 개선 (v1.5.0 신규)
- ✅ **모듈화**: 코드를 기능별 모듈로 분리 (core, managers, ui, utils)
- ✅ **문서화**: 5개의 상세 개발자 문서 작성 (총 3800줄)
- ✅ **유지보수성**: 파일당 평균 150줄로 관리 용이
- ✅ **확장성**: 명확한 책임 분담 및 확장 가이드 제공

---

## 🔧 주요 클래스 구조 (v1.5.0 모듈화)

### 📂 프로젝트 구조
```
src/
├── main.py (50줄)              # 진입점
└── pdfmask/
    ├── core/                    # 데이터 모델
    │   └── models.py           # MaskEntry
    ├── managers/                # 비즈니스 로직
    │   ├── license_manager.py  # 라이선스 인증
    │   ├── pdf_manager.py      # PDF 처리
    │   ├── mask_data_manager.py # 데이터 영속화
    │   ├── progress_manager.py # 진행상황 관리
    │   └── log_manager.py      # 로그 관리
    ├── ui/                      # UI 컴포넌트
    │   ├── main_window.py      # 메인 윈도우
    │   ├── pdf_view.py         # PDF 뷰어
    │   └── dialogs.py          # 다이얼로그
    └── utils/                   # 유틸리티
```

### Core 모듈 (`pdfmask.core`)

**MaskEntry (dataclass)**
- 마스킹 정보 데이터 구조
- 페이지 인덱스, 좌표, 메모 저장

### Managers 모듈 (`pdfmask.managers`)

**PdfDocumentManager**
- PDF 로드, 페이지 렌더링 (zoom 지원)
- Redaction 적용 및 저장

**LicenseManager** (`license_manager.py`)
```python
is_licensed() -> bool
validate_serial(serial: str) -> Tuple[bool, str]
activate_license(serial: str) -> Tuple[bool, str]
deactivate_license() -> None
```
- 라이선스 파일: `.license` (JSON)
- 시리얼 형식: XXXX-XXXX-XXXX-XXXX
- SHA256 해시로 저장

**MaskDataManager** (`mask_data_manager.py`)
```python
save_masks(pdf_path: str, masks: List[MaskEntry]) -> Tuple[bool, str]
load_masks(pdf_path: str) -> Tuple[bool, List[MaskEntry], str]
delete_masks(pdf_path: str) -> Tuple[bool, str]
```
- 일자별 통합 JSON 파일 (`mask_data_YYYYMMDD.json`)
- 파일명을 키로 사용

**ProgressManager** (`progress_manager.py`)
```python
save_progress(...) -> Tuple[bool, str]
load_progress() -> Tuple[bool, Dict, str]
clear_progress() -> Tuple[bool, str]
```
- 폴더 작업 진행 상황 추적 (`progress.json`)
- 완료 파일 목록 관리

**LogManager** (`log_manager.py`)
```python
log_app_start() / log_app_end()
log_pdf_open(file_path)
log_folder_open(folder_path, file_count)
log_mask_save(file_path, masks)  # 상세 좌표 포함
log_error(operation, error_message)
```
- 일자별 로그 파일 (`pdfmask_YYYYMMDD.log`)
- UTF-8 인코딩 (한글 지원)

### UI 모듈 (`pdfmask.ui`)

**MainWindow** (`main_window.py`)
- UI 관리 및 워크플로우 제어
- 이벤트 처리 및 데이터 동기화
- 메뉴, 툴바, 단축키 관리

**PdfPageView** (`pdf_view.py`)
- 마우스 드래그 마스킹 선택
- 화면 ↔ PDF 좌표 변환
- 마스킹 영역 시각화

**ScrollablePdfView** (`pdf_view.py`)
- 스크롤 및 줌 기능
- PDF 페이지 컨테이너

**SerialInputDialog** (`dialogs.py`)
- 라이선스 인증 다이얼로그
- 시리얼 번호 입력 및 검증

---

## 💾 데이터 구조

### MaskEntry (dataclass)
```python
@dataclass
class MaskEntry:
    page_index: int      # 0-based (내부), 1-based (UI)
    rect: fitz.Rect      # PDF 좌표계
    note: str = ""       # 사용자 메모
```

### JSON 파일 구조

**mask_data_20251118.json**
```json
{
  "D:/Documents/file1.pdf": [
    {"page_index": 0, "rect": [100.5, 200.3, 300.7, 250.6], "note": "주민등록번호"},
    {"page_index": 0, "rect": [150.2, 400.1, 350.8, 450.5], "note": "전화번호"}
  ]
}
```

**progress.json**
```json
{
  "folder_path": "D:/Documents/contracts",
  "pdf_files": ["file1.pdf", "file2.pdf"],
  "completed_files": ["file1.pdf"],
  "current_index": 1,
  "last_update": "2025-11-18T14:30:00"
}
```

**로그 예시 (pdfmask_20251118.log)**
```
2025-11-18 09:35:10 [INFO] Mask Saved: D:/test.pdf (2 masks)
2025-11-18 09:35:10 [INFO]   Mask #1: Page 1, Rect(100.50, 200.30, 300.75, 250.60), Note: 주민등록번호
2025-11-18 09:35:10 [INFO]   Mask #2: Page 1, Rect(150.20, 400.10, 350.80, 450.50), Note: 전화번호
```

---

## 🎯 주요 워크플로우

### 저장 프로세스
```
1. Ctrl+S 누름
   ↓
2. 백업 수행 (활성화 시) → backup/YYYYMMDD/
   ↓
3. PyMuPDF Redaction 적용 (흰색, 영구 제거)
   ↓
4. 마스킹 데이터 저장 → mask_data_YYYYMMDD.json
   ↓
5. 진행 상황 저장 → progress.json
   ↓
6. 로그 기록 → pdfmask_YYYYMMDD.log
   ↓
7. 다음 파일 이동 제안
```

### 폴더 작업 복구
```
1. 폴더 열기 (Ctrl+Shift+O)
   ↓
2. progress.json 확인
   ↓
3. "이전 작업을 이어하시겠습니까?" 다이얼로그
   ↓
4. [예] → 완료 파일 ✓ 표시, 다음 파일부터 시작
   [아니요] → 처음부터 새로 시작
```

---

## ⌨️ 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+O` | PDF 파일 열기 |
| `Ctrl+Shift+O` | 폴더 열기 |
| `Ctrl+S` | 마스킹 저장 |
| `Ctrl+드래그` | 마스킹 영역 선택 |
| `Ctrl+휠` | 확대/축소 (50%~200%) |
| `←/→` | 이전/다음 페이지 |
| `PageUp/Down` | 이전/다음 페이지 |
| `Del` | 마스킹 삭제 |
| `더블클릭` | 메모 편집 |

---

## 🔍 주요 기술 구현

### 1. 좌표 변환 시스템
```python
# 화면 → PDF
scale_x = page_width / pixmap.width()
pdf_x = screen_x * scale_x

# PDF → 화면
scale_x = pixmap.width() / page_width
screen_x = int(pdf_x * scale_x)
```

### 2. PyMuPDF Redaction
```python
# 마스킹 영역에 redaction annotation 추가
page.add_redact_annot(rect, fill=(1, 1, 1))  # 흰색

# 실제로 내용 제거 및 적용
     page.apply_redactions()

# Incremental 저장
   doc.save(path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
```

### 3. 시그널/슬롯 패턴
```python
class PdfPageView(QWidget):
    maskCreated = pyqtSignal(int, object)  # (page_index, fitz.Rect)
    
    def mouseReleaseEvent(self, event):
        pdf_rect = self._convert_to_pdf_rect(screen_rect)
        self.maskCreated.emit(self._page_index, pdf_rect)
```

---

## 📂 파일 구조 (v1.5.0)
```
pdfmask/
├── src/                       # 소스 코드
│   ├── main.py               # 애플리케이션 진입점 (50줄)
│   └── pdfmask/              # 메인 패키지
│       ├── core/             # 데이터 모델
│       ├── managers/         # 비즈니스 로직 (5개 파일)
│       ├── ui/               # UI 컴포넌트 (3개 파일)
│       └── utils/            # 유틸리티
│
├── docs/                      # 개발자 문서
│   ├── SPECIFICATION.md      # 기능 명세서 (1500줄)
│   ├── ARCHITECTURE.md       # 아키텍처 문서 (800줄)
│   ├── PROJECT_SUMMARY.md    # 프로젝트 요약 (600줄)
│   ├── REFACTORING_SUMMARY.md # 리팩토링 요약 (500줄)
│   └── QUICK_START.md        # 빠른 시작 가이드 (400줄)
│
├── backup/                    # PDF 백업 (일자별, 자동 생성)
│   └── YYYYMMDD/*.pdf
│
├── masks_data/                # 마스킹 데이터 (일자별, 자동 생성)
│   └── mask_data_YYYYMMDD.json
│
├── logs/                      # 로그 파일 (일자별, 자동 생성)
│   └── pdfmask_YYYYMMDD.log
│
├── progress.json              # 진행 상황 (자동 생성/삭제)
├── .license                   # 라이선스 파일
├── pyproject.toml             # 프로젝트 설정
├── README.md                  # 사용자 가이드
├── DEVLOG.md                  # 개발 로그 (본 문서)
└── main.py.backup             # 이전 버전 백업
```

---

## 🐛 문제 해결 이력

### PyQt5 → PyQt6 마이그레이션
- **문제**: Windows 환경에서 PyQt5 설치 실패
- **해결**: PyQt6로 변경, Enum 값 및 Import 경로 수정

### Permission Denied 에러
- **문제**: PDF 저장 시 "Permission denied" 의미 없는 메시지
- **해결**: 명확한 에러 메시지 제공 ("다른 프로그램에서 열려 있습니다")

### 백업 폴더 위치
- **변경 전**: PDF와 같은 폴더
- **변경 후**: 프로젝트 최상단 `backup/` 폴더

### 마스킹 데이터 저장 구조
- **변경 전**: 파일별 개별 JSON
- **변경 후**: 일자별 통합 JSON (파일별 리스트 구조)

### Git 커밋 메시지 인코딩
- **문제**: PowerShell에서 한글 커밋 메시지 깨짐
- **해결**: 영어 커밋 메시지 사용

---

## 🔧 의존성
```toml
dependencies = [
    "pymupdf>=1.26.6",    # PDF 처리
    "pyqt6>=6.5.0",       # GUI
    "openpyxl>=3.1.0",    # Excel (향후 사용)
]
```

---

## 📊 향후 개선 가능 항목

### 우선순위 높음
- [ ] 실제 라이선스 서버 API 연동
- [ ] 네트워크 오류 처리 강화
- [ ] 머신 ID 기반 인증

### 우선순위 중간
- [ ] 엑셀 저장 기능 (마스킹 작업 내역)
- [ ] 로그 파일 자동 압축 및 보관 정책
- [ ] 마스킹 색상 선택 옵션
- [ ] 확대 기능 오류 수정 (보류 중)

### 우선순위 낮음
- [ ] 실행 취소/다시 실행 기능
- [ ] 배치 처리 모드
- [ ] 라이선스 정보 보기/재인증
- [ ] 로그 뷰어 및 통계 대시보드

---

## ⚠️ 주의사항

1. **영구 마스킹**: Redaction은 원본 데이터를 완전히 제거하며 복구 불가능
2. **백업 권장**: 중요한 파일은 반드시 백업 기능 활성화
3. **파일 잠금**: PDF를 다른 프로그램에서 열고 있으면 저장 실패
4. **페이지 인덱스**: 내부는 0-based, UI 표시는 1-based

---

## 📝 테스트 시나리오

### 기본 기능 테스트
1. PDF 파일 열기 → 페이지 렌더링 확인
2. Ctrl+드래그 → 마스킹 선택 확인 (파란색 → 빨간색)
3. 더블클릭 → 메모 편집 확인
4. Ctrl+S → 저장 및 Redaction 적용 확인

### 폴더 작업 테스트
1. 폴더 열기 → 파일 목록 표시 확인
2. 일부 파일 작업 후 프로그램 종료
3. 재시작 → "이전 작업을 이어하시겠습니까?" 확인
4. 완료 파일 ✓ 표시 확인

### 데이터 관리 테스트
1. 백업 폴더 생성 확인 (`backup/YYYYMMDD/`)
2. JSON 파일 생성 확인 (`mask_data_YYYYMMDD.json`)
3. 로그 파일 생성 확인 (`pdfmask_YYYYMMDD.log`)
4. 저장한 PDF 다시 열기 → 마스킹 데이터 복원 확인

---

## 📖 개발 참고

### PyQt6 주요 변경사항
- `Qt.AlignCenter` → `Qt.AlignmentFlag.AlignCenter`
- `QAction`: `QtWidgets` → `QtGui`
- `app.exec_()` → `app.exec()`

### PyMuPDF 주요 메서드
- `fitz.open(path)`: PDF 열기
- `page.get_pixmap(matrix=mat)`: 페이지 렌더링
- `page.add_redact_annot(rect, fill)`: Redaction 추가
- `page.apply_redactions()`: Redaction 적용

### Python logging
- `FileHandler(file, encoding='utf-8')`: UTF-8 로그
- `Formatter('%(asctime)s [%(levelname)s] %(message)s')`: 포맷

---

## 버전 히스토리

### v1.5.0 (2025-11-19) - 리팩토링 및 문서화
- ✨ **프로젝트 모듈화**: 단일 파일(2000줄) → 모듈별 분리(평균 150줄)
- 📚 **문서화 완료**: 5개의 개발자 문서 작성 (총 3800줄)
  - SPECIFICATION.md (기능 명세서)
  - ARCHITECTURE.md (아키텍처 문서)
  - PROJECT_SUMMARY.md (프로젝트 요약)
  - REFACTORING_SUMMARY.md (리팩토링 요약)
  - QUICK_START.md (빠른 시작 가이드)
- 🔧 **유지보수성 향상**: 명확한 책임 분담, 확장 가이드
- 📂 **구조 개선**: core, managers, ui, utils 모듈 분리
- 📖 **온보딩 개선**: 새 개발자를 위한 상세 가이드

### v1.5 (2025-11-18) - 데이터 관리 강화
- ✨ PDF 자동 백업 기능
- ✨ 라이선스 인증 시스템
- ✨ 마스킹 데이터 JSON 저장
- ✨ 진행 상황 추적 및 복구
- ✨ 상세 로그 기록
- 🔧 도움말 메뉴 추가
- 🔧 툴바 아이콘 추가

### v1.0 (2025-11-17) - 첫 번째 릴리스
- 🎉 첫 번째 정식 릴리스
- ✅ 기본 마스킹 기능
- ✅ 폴더 일괄 처리
- ✅ UI/UX 최적화

---

## 📊 프로젝트 통계 (v1.5.0)

### 코드 라인 수
- **총 Python 코드**: ~2000줄 (변경 없음)
- **main.py**: 2000줄 → 50줄 (95% 감소)
- **모듈 파일**: 0개 → 13개
- **평균 파일 크기**: 2000줄 → 150줄

### 문서 라인 수
- **개발자 문서**: 0줄 → 3800줄
- **README.md**: 업데이트됨
- **DEVLOG.md**: 업데이트됨

### 모듈 구성
- **core**: 1개 파일 (MaskEntry)
- **managers**: 5개 파일 (5개 Manager)
- **ui**: 3개 파일 (4개 클래스)
- **utils**: 준비됨 (향후 확장)

---

**PDF Mask v1.5.0** - 유지보수 가능한 전문적인 PDF 개인정보 마스킹 솔루션
