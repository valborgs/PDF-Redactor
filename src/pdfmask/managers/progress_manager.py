"""
작업 진행상황 관리 모듈
"""

import os
import json
from datetime import datetime
from typing import Tuple, List, Dict


class ProgressManager:
    """
    폴더 일괄 작업 시 진행상황을 추적하는 클래스
    
    progress.json 파일에 현재 작업 상태를 저장합니다.
    """
    
    def __init__(self) -> None:
        """
        초기화
        
        프로젝트 루트의 progress.json 파일을 관리합니다.
        """
        # 프로젝트 루트 경로 (src/pdfmask/managers/ -> src/ -> project_root/)
        current_file = os.path.abspath(__file__)
        managers_dir = os.path.dirname(current_file)  # managers/
        pdfmask_dir = os.path.dirname(managers_dir)   # pdfmask/
        src_dir = os.path.dirname(pdfmask_dir)        # src/
        self.project_root = os.path.dirname(src_dir)  # project_root/
        self.progress_file = os.path.join(self.project_root, "progress.json")
    
    def save_progress(
        self,
        folder_path: str,
        pdf_files: List[str],
        completed_files: List[str],
        current_index: int
    ) -> Tuple[bool, str]:
        """
        작업 진행상황 저장
        
        Args:
            folder_path: 작업 중인 폴더 경로
            pdf_files: 전체 PDF 파일 리스트
            completed_files: 완료된 파일 리스트
            current_index: 현재 작업 중인 파일 인덱스
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            data = {
                'folder_path': folder_path,
                'last_updated': datetime.now().isoformat(),
                'total_files': len(pdf_files),
                'completed_count': len(completed_files),
                'current_index': current_index,
                'pdf_files': [os.path.basename(f) for f in pdf_files],
                'completed_files': completed_files,
            }
            
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True, "진행상황 저장 완료"
            
        except Exception as e:
            return False, f"진행상황 저장 실패: {str(e)}"
    
    def load_progress(self) -> Tuple[bool, Dict, str]:
        """
        작업 진행상황 로드
        
        Returns:
            Tuple[bool, Dict, str]: (성공 여부, 진행상황 데이터, 메시지)
        """
        try:
            if not os.path.exists(self.progress_file):
                return True, {}, "진행상황 파일 없음"
            
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return True, data, "진행상황 로드 완료"
            
        except Exception as e:
            return False, {}, f"진행상황 로드 실패: {str(e)}"
    
    def clear_progress(self) -> Tuple[bool, str]:
        """
        작업 진행상황 삭제
        
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            if os.path.exists(self.progress_file):
                os.remove(self.progress_file)
                return True, "진행상황 삭제 완료"
            else:
                return True, "진행상황 파일 없음"
                
        except Exception as e:
            return False, f"진행상황 삭제 실패: {str(e)}"

