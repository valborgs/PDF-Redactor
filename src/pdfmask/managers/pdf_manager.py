"""
PDF 문서 관리 모듈
"""

import fitz  # PyMuPDF
from typing import Optional
from PyQt6.QtGui import QPixmap, QImage

from ..core.models import MaskEntry


class PdfDocumentManager:
    """
    PDF 문서 로드, 렌더링, 마스킹 적용 클래스
    
    PyMuPDF를 사용하여 PDF 파일을 처리합니다.
    """

    def __init__(self) -> None:
        """
        초기화
        """
        self.doc: Optional[fitz.Document] = None
        self.file_path: Optional[str] = None

    def load_pdf(self, path: str) -> None:
        """
        PDF 파일 로드
        
        Args:
            path: PDF 파일 경로
            
        Raises:
            Exception: PDF 파일 로드 실패 시
        """
        try:
            # 기존 문서가 있다면 닫기
            if self.doc is not None:
                self.doc.close()
                self.doc = None

            # 새 문서 열기
            self.doc = fitz.open(path)
            self.file_path = path
            
        except Exception as e:
            self.doc = None
            self.file_path = None
            raise Exception(f"PDF 파일을 열 수 없습니다: {str(e)}")

    def get_page_count(self) -> int:
        """
        전체 페이지 수 반환
        
        Returns:
            int: 페이지 수
        """
        if self.doc is None:
            return 0
        return len(self.doc)

    def get_page_pixmap(self, page_index: int, zoom: float = 1.5) -> Optional[QPixmap]:
        """
        지정된 페이지를 QPixmap으로 렌더링
        
        Args:
            page_index: 페이지 인덱스 (0-based)
            zoom: 확대/축소 배율
            
        Returns:
            Optional[QPixmap]: 렌더링된 QPixmap 객체 또는 None
        """
        if self.doc is None:
            return None

        try:
            # 페이지 범위 체크
            if page_index < 0 or page_index >= len(self.doc):
                return None

            # 페이지 로드
            page = self.doc.load_page(page_index)

            # 확대/축소 매트릭스 적용하여 렌더링
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # PyMuPDF Pixmap을 QImage로 변환
            img_data = pix.samples
            img = QImage(
                img_data,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format.Format_RGB888
            )

            # QImage를 QPixmap으로 변환
            return QPixmap.fromImage(img)

        except Exception as e:
            print(f"페이지 렌더링 오류: {str(e)}")
            return None

    def apply_masks_and_save(self, masks: list[MaskEntry]) -> None:
        """
        마스킹을 PDF에 적용하고 저장
        
        PyMuPDF의 Redaction 기능을 사용하여 영구적으로 마스킹합니다.
        
        Args:
            masks: 적용할 마스킹 정보 리스트
            
        Raises:
            Exception: 문서가 없거나 저장 중 오류 발생 시
        """
        if self.doc is None or self.file_path is None:
            raise Exception("열린 PDF 문서가 없습니다.")
        
        try:
            # 페이지별로 마스크 적용
            for page_num in range(len(self.doc)):
                # 현재 페이지의 마스크만 필터링
                page_masks = [m for m in masks if m.page_index == page_num]
                
                if not page_masks:
                    continue
                
                # 페이지 로드
                page = self.doc.load_page(page_num)
                
                # 각 마스크에 대해 redaction annotation 추가
                for mask in page_masks:
                    # 흰색으로 마스킹 (1, 1, 1) = RGB white
                    page.add_redact_annot(mask.rect, fill=(1, 1, 1))
                
                # 페이지별로 redaction 적용
                page.apply_redactions()
                
                print(f"페이지 {page_num + 1}에 {len(page_masks)}개의 마스크 적용 완료")
            
            print("모든 페이지의 Redaction 적용 완료")
            
            # 파일 저장 (incremental 저장)
            self.doc.save(
                self.file_path,
                incremental=True,
                encryption=fitz.PDF_ENCRYPT_KEEP
            )
            print(f"파일 저장 완료: {self.file_path}")
            
        except Exception as e:
            error_msg = str(e)
            # Permission denied 오류 확인
            if "Permission denied" in error_msg or "permission denied" in error_msg.lower():
                raise Exception(
                    "파일 저장 권한이 없습니다.\n\n"
                    "PDF 파일이 다른 프로그램(Adobe Reader, 웹 브라우저 등)에서 열려있을 수 있습니다.\n"
                    "해당 프로그램을 종료한 후 다시 시도해주세요.\n\n"
                    f"파일 경로: {self.file_path}"
                )
            else:
                raise Exception(f"마스킹 저장 중 오류 발생: {error_msg}")

    def close(self) -> None:
        """
        문서 닫기
        """
        if self.doc is not None:
            self.doc.close()
            self.doc = None
        self.file_path = None

