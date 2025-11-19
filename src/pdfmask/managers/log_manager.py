"""
로그 관리 모듈
"""

import os
import logging
from datetime import datetime
from typing import List

from ..core.models import MaskEntry


class LogManager:
    """
    애플리케이션 로그를 일자별로 기록하는 클래스
    
    logs 폴더에 pdfmask_YYYYMMDD.log 형식으로 저장합니다.
    """
    
    def __init__(self) -> None:
        """
        초기화
        
        로그 폴더를 생성하고 로거를 설정합니다.
        """
        # 프로젝트 루트 경로 (src/pdfmask/managers/ -> src/ -> project_root/)
        current_file = os.path.abspath(__file__)
        managers_dir = os.path.dirname(current_file)  # managers/
        pdfmask_dir = os.path.dirname(managers_dir)   # pdfmask/
        src_dir = os.path.dirname(pdfmask_dir)        # src/
        self.project_root = os.path.dirname(src_dir)  # project_root/
        self.logs_dir = os.path.join(self.project_root, "logs")
        
        # 로그 폴더 생성
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # 일자별 로그 파일 설정
        self.setup_logger()
    
    def setup_logger(self) -> None:
        """
        로거 설정 (일자별 로그 파일)
        """
        today_str = datetime.now().strftime("%Y%m%d")
        log_filename = f"pdfmask_{today_str}.log"
        log_filepath = os.path.join(self.logs_dir, log_filename)
        
        # 기존 핸들러 제거
        logger = logging.getLogger('PDFMask')
        logger.handlers.clear()
        
        # 로거 레벨 설정
        logger.setLevel(logging.INFO)
        
        # 파일 핸들러
        file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 포맷 설정
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
        self.logger = logger
    
    def info(self, message: str) -> None:
        """정보 로그"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """경고 로그"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """에러 로그"""
        self.logger.error(message)
    
    def log_app_start(self) -> None:
        """프로그램 시작 로그"""
        self.info("=" * 60)
        self.info("PDF Mask Application Started")
        self.info("=" * 60)
    
    def log_app_end(self) -> None:
        """프로그램 종료 로그"""
        self.info("=" * 60)
        self.info("PDF Mask Application Closed")
        self.info("=" * 60)
    
    def log_license_check(self, success: bool, message: str) -> None:
        """라이선스 인증 로그"""
        if success:
            self.info(f"License Check: SUCCESS - {message}")
        else:
            self.warning(f"License Check: FAILED - {message}")
    
    def log_pdf_open(self, file_path: str) -> None:
        """PDF 파일 열기 로그"""
        self.info(f"PDF Opened: {file_path}")
    
    def log_folder_open(self, folder_path: str, file_count: int) -> None:
        """폴더 열기 로그"""
        self.info(f"Folder Opened: {folder_path} ({file_count} PDF files)")
    
    def log_mask_save(self, file_path: str, masks: List[MaskEntry]) -> None:
        """마스킹 저장 로그"""
        self.info(f"Mask Saved: {file_path} ({len(masks)} masks)")
        
        # 각 마스킹 영역 상세 정보 기록
        for i, mask in enumerate(masks, 1):
            rect = mask.rect
            note = mask.note if mask.note else "(no note)"
            self.info(
                f"  Mask #{i}: Page {mask.page_index + 1}, "
                f"Rect({rect.x0:.2f}, {rect.y0:.2f}, {rect.x1:.2f}, {rect.y1:.2f}), "
                f"Note: {note}"
            )
    
    def log_error(self, operation: str, error_message: str) -> None:
        """에러 로그"""
        self.error(f"Error in {operation}: {error_message}")

