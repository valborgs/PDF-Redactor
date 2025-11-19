"""
데이터 모델 정의
"""

from dataclasses import dataclass
import fitz  # PyMuPDF


@dataclass
class MaskEntry:
    """
    마스킹 정보 데이터 클래스
    
    Attributes:
        page_index (int): 페이지 인덱스 (0-based)
        rect (fitz.Rect): 마스킹 영역 좌표 (PDF 좌표계)
        note (str): 사용자 메모
    """
    page_index: int
    rect: fitz.Rect
    note: str = ""

