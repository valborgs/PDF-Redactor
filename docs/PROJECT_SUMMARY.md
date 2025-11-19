# PDF Mask 프로젝트 요약

## 📋 빠른 참조 가이드

### 사용자용 문서
- **[README.md](README.md)**: 사용자 가이드, 설치 및 사용 방법

### 개발자용 문서
- **[SPECIFICATION.md](SPECIFICATION.md)**: 전체 기능 명세서, 클래스 및 메서드 상세 설명
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: 아키텍처 개요, 설계 원칙, 확장 가이드
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: 본 문서 - 프로젝트 전체 요약

---

## 🎯 프로젝트 개요

**PDF Mask**는 PDF 문서의 민감한 정보를 영구적으로 마스킹하는 PyQt6 기반 데스크톱 애플리케이션입니다.

### 핵심 기능
✅ Ctrl + 드래그로 마스킹 영역 선택  
✅ PyMuPDF Redaction으로 영구 제거  
✅ 일자별 자동 백업  
✅ 폴더 일괄 처리  
✅ 진행상황 복구  
✅ JSON/Excel 작업 이력 관리  
✅ 라이선스 인증  

---

## 📁 프로젝트 구조 한눈에 보기

```
pdfmask/
│
├── 📂 src/                          # 소스 코드
│   ├── 🚀 main.py                   # 진입점
│   └── 📦 pdfmask/                  # 메인 패키지
│       ├── 🧩 core/                 # 데이터 모델
│       │   └── models.py            # MaskEntry
│       │
│       ├── ⚙️ managers/              # 비즈니스 로직
│       │   ├── license_manager.py   # 라이선스 인증
│       │   ├── pdf_manager.py       # PDF 처리
│       │   ├── mask_data_manager.py # 데이터 영속화
│       │   ├── progress_manager.py  # 진행상황 관리
│       │   └── log_manager.py       # 로그 관리
│       │
│       ├── 🎨 ui/                    # 사용자 인터페이스
│       │   ├── main_window.py       # 메인 윈도우
│       │   ├── pdf_view.py          # PDF 뷰어
│       │   └── dialogs.py           # 다이얼로그
│       │
│       └── 🔧 utils/                 # 유틸리티
│
├── 📂 backup/                       # 백업 폴더 (자동 생성)
├── 📂 masks_data/                   # 마스킹 데이터 (자동 생성)
├── 📂 logs/                         # 로그 (자동 생성)
│
├── 📄 pyproject.toml                # 프로젝트 설정
├── 📄 README.md                     # 사용자 가이드
├── 📄 SPECIFICATION.md              # 기능 명세서
├── 📄 ARCHITECTURE.md               # 아키텍처 문서
└── 📄 PROJECT_SUMMARY.md            # 본 문서
```

---

## 🔧 기술 스택

| 구분 | 기술 | 버전 | 용도 |
|------|------|------|------|
| **언어** | Python | 3.12+ | 메인 프로그래밍 언어 |
| **GUI** | PyQt6 | 6.5.0+ | 사용자 인터페이스 |
| **PDF** | PyMuPDF (fitz) | 1.26.6+ | PDF 처리 및 Redaction |
| **Excel** | openpyxl | 3.1.5+ | 작업 내역 엑셀 저장 |
| **패키지 관리** | uv | - | 의존성 관리 |

---

## 📊 모듈 책임 분담

### 1️⃣ Core Module (핵심 데이터)
- **책임**: 데이터 구조 정의
- **파일**: `models.py`
- **클래스**: `MaskEntry`

### 2️⃣ Managers Module (비즈니스 로직)
- **책임**: 각 도메인별 로직 처리
- **파일**: `license_manager.py`, `pdf_manager.py`, `mask_data_manager.py`, `progress_manager.py`, `log_manager.py`
- **클래스**: 5개 Manager 클래스

### 3️⃣ UI Module (사용자 인터페이스)
- **책임**: GUI 컴포넌트 및 이벤트 처리
- **파일**: `main_window.py`, `pdf_view.py`, `dialogs.py`
- **클래스**: `MainWindow`, `PdfPageView`, `ScrollablePdfView`, `SerialInputDialog`

### 4️⃣ Utils Module (유틸리티)
- **책임**: 공통 함수 (향후 확장)
- **파일**: 현재 비어있음

---

## 🔄 주요 데이터 흐름

### 1. 애플리케이션 시작
```
main.py → LicenseManager → (인증) → MainWindow → LogManager
```

### 2. PDF 열기 및 마스킹
```
사용자 → open_pdf() → PdfDocumentManager.load_pdf() 
      → MaskDataManager.load_masks()
      → update_page_view()
      → PdfPageView.set_page()

사용자 (Ctrl+드래그) → PdfPageView 마우스 이벤트 
                    → maskCreated 시그널
                    → MainWindow.on_mask_created()
                    → masks 리스트 업데이트
```

### 3. 마스킹 저장
```
사용자 (Ctrl+S) → save_masks()
               → backup_current_pdf() (옵션)
               → MaskDataManager.save_masks()
               → PdfDocumentManager.apply_masks_and_save()
               → export_masks_to_excel()
               → LogManager.log_mask_save()
               → ProgressManager.save_progress()
               → 다음 파일로 이동
```

---

## 🎓 새 개발자 온보딩 가이드

### Step 1: 프로젝트 클론 및 설치
```bash
git clone https://github.com/yourusername/pdfmask.git
cd pdfmask
uv sync
```

### Step 2: 실행 및 테스트
```bash
uv run python src/main.py
# 테스트 시리얼: TEST-1234-5678-ABCD
```

### Step 3: 문서 읽기 순서
1. **[README.md](README.md)** - 사용자 관점 이해
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - 전체 구조 파악
3. **[SPECIFICATION.md](SPECIFICATION.md)** - 상세 기능 학습

### Step 4: 코드 탐색 순서
1. `src/main.py` - 진입점 이해
2. `src/pdfmask/core/models.py` - 데이터 구조
3. `src/pdfmask/managers/` - 비즈니스 로직 (하나씩)
4. `src/pdfmask/ui/main_window.py` - UI 로직

### Step 5: 첫 기여
- 간단한 버그 수정 또는 기능 추가
- Pull Request 작성

---

## 🛠️ 주요 클래스 빠른 참조

| 클래스 | 파일 | 주요 메서드 | 설명 |
|--------|------|-------------|------|
| **MaskEntry** | `core/models.py` | - | 마스킹 정보 데이터 클래스 |
| **LicenseManager** | `managers/license_manager.py` | `is_licensed()`, `activate_license()` | 라이선스 인증 |
| **PdfDocumentManager** | `managers/pdf_manager.py` | `load_pdf()`, `get_page_pixmap()`, `apply_masks_and_save()` | PDF 처리 |
| **MaskDataManager** | `managers/mask_data_manager.py` | `save_masks()`, `load_masks()` | 데이터 영속화 |
| **ProgressManager** | `managers/progress_manager.py` | `save_progress()`, `load_progress()` | 진행상황 관리 |
| **LogManager** | `managers/log_manager.py` | `log_app_start()`, `log_mask_save()` | 로그 기록 |
| **MainWindow** | `ui/main_window.py` | `open_pdf()`, `save_masks()` | 메인 윈도우 |
| **PdfPageView** | `ui/pdf_view.py` | `set_page()`, `mousePressEvent()` | PDF 뷰어 |
| **SerialInputDialog** | `ui/dialogs.py` | `activate()` | 라이선스 다이얼로그 |

---

## 📝 자주 수정하는 코드 위치

### UI 변경
- **메뉴 추가**: `MainWindow.setup_menu()`
- **단축키 추가**: `MainWindow.setup_shortcuts()`
- **툴바 버튼 추가**: `MainWindow.setup_toolbar()`
- **레이아웃 변경**: `MainWindow.init_ui()`

### 비즈니스 로직 변경
- **저장 프로세스**: `MainWindow.save_masks()`
- **PDF 렌더링**: `PdfDocumentManager.get_page_pixmap()`
- **마스킹 적용**: `PdfDocumentManager.apply_masks_and_save()`

### 데이터 구조 변경
- **MaskEntry 필드 추가**: `core/models.py`
- **JSON 포맷 변경**: `MaskDataManager.save_masks()`, `load_masks()`

---

## 🐛 디버깅 체크리스트

### 1. 로그 확인
```bash
# 로그 파일 위치
logs/pdfmask_YYYYMMDD.log
```

### 2. 마스킹 데이터 확인
```bash
# JSON 파일 위치
masks_data/mask_data_YYYYMMDD.json
```

### 3. 진행상황 확인
```bash
# 진행상황 파일
progress.json
```

### 4. 라이선스 상태 확인
```bash
# 라이선스 파일
.license
```

### 5. 일반적인 문제
| 문제 | 원인 | 해결 |
|------|------|------|
| "Permission denied" | PDF 파일 잠금 | 다른 프로그램에서 PDF 닫기 |
| 마스킹 드래그 안됨 | Ctrl 키 누르지 않음 | Ctrl + 드래그 |
| 확대/축소 안됨 | Ctrl 키 누르지 않음 | Ctrl + 휠 |
| 라이선스 인증 실패 | 잘못된 시리얼 | 테스트 시리얼 사용 |

---

## 🚀 기능 확장 예시

### 예시 1: 템플릿 기능 추가

**1. Manager 추가**
```python
# src/pdfmask/managers/template_manager.py
class TemplateManager:
    def save_template(self, name: str, masks: List[MaskEntry]) -> bool:
        pass
```

**2. UI 추가**
```python
# src/pdfmask/ui/template_dialog.py
class TemplateDialog(QDialog):
    pass
```

**3. MainWindow 통합**
```python
# MainWindow.__init__()
self.template_manager = TemplateManager()
```

### 예시 2: OCR 기능 추가

**1. Utils 추가**
```python
# src/pdfmask/utils/ocr_utils.py
def extract_text_regions(page: fitz.Page) -> List[fitz.Rect]:
    pass
```

**2. Manager 활용**
```python
# PdfDocumentManager에 메서드 추가
def find_text_regions(self, search_text: str) -> List[MaskEntry]:
    pass
```

---

## 📚 추가 리소스

### 공식 문서
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)

### 프로젝트 문서
- **사용자 가이드**: [README.md](README.md)
- **기능 명세서**: [SPECIFICATION.md](SPECIFICATION.md)
- **아키텍처**: [ARCHITECTURE.md](ARCHITECTURE.md)

### 커뮤니티
- GitHub Issues: 버그 리포트 및 기능 제안
- Pull Requests: 코드 기여

---

## ✅ 체크리스트

### 코드 작성 전
- [ ] SPECIFICATION.md에서 해당 기능 확인
- [ ] ARCHITECTURE.md에서 모듈 책임 확인
- [ ] 기존 코드 스타일 확인

### 코드 작성 후
- [ ] 타입 힌트 추가
- [ ] Docstring 작성
- [ ] 에러 핸들링 추가
- [ ] 로그 기록 추가 (필요시)

### 테스트
- [ ] 수동 테스트 수행
- [ ] 로그 파일 확인
- [ ] 다양한 PDF 파일로 테스트

### 문서 업데이트
- [ ] SPECIFICATION.md 업데이트 (기능 추가 시)
- [ ] README.md 업데이트 (사용자 영향 시)
- [ ] ARCHITECTURE.md 업데이트 (구조 변경 시)

---

## 📞 연락처 및 지원

- **이슈 보고**: GitHub Issues
- **기능 제안**: GitHub Discussions
- **긴급 문의**: [이메일 주소]

---

**PDF Mask v1.5** - 빠른 온보딩을 위한 프로젝트 요약

