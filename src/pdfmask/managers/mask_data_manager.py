"""
마스킹 데이터 관리 모듈
"""

import os
import json
import fitz
from datetime import datetime
from typing import Tuple, List

from ..core.models import MaskEntry


class MaskDataManager:
    """
    마스킹 데이터를 일자별 JSON 파일로 저장/로드하는 클래스
    """
    
    def __init__(self) -> None:
        """
        초기화
        
        프로젝트 루트의 masks_data 폴더에 데이터를 저장합니다.
        """
        # 프로젝트 루트 경로 (src/pdfmask/managers/ -> src/ -> project_root/)
        current_file = os.path.abspath(__file__)
        managers_dir = os.path.dirname(current_file)  # managers/
        pdfmask_dir = os.path.dirname(managers_dir)   # pdfmask/
        src_dir = os.path.dirname(pdfmask_dir)        # src/
        self.project_root = os.path.dirname(src_dir)  # project_root/
        self.masks_dir = os.path.join(self.project_root, "masks_data")
        
        # 마스킹 데이터 폴더 생성
        os.makedirs(self.masks_dir, exist_ok=True)
    
    def get_mask_file_path(self) -> str:
        """
        일자별 마스킹 데이터 파일 경로 반환
        
        Returns:
            str: 마스킹 데이터 파일 경로 (masks_data/mask_data_YYYYMMDD.json)
        """
        today_str = datetime.now().strftime("%Y%m%d")
        mask_filename = f"mask_data_{today_str}.json"
        return os.path.join(self.masks_dir, mask_filename)
    
    def save_masks(self, pdf_path: str, masks: List[MaskEntry]) -> Tuple[bool, str]:
        """
        마스킹 데이터를 일자별 JSON 파일에 추가 저장
        
        Args:
            pdf_path: PDF 파일 경로
            masks: 마스킹 데이터 리스트
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지 또는 파일 경로)
        """
        try:
            mask_file = self.get_mask_file_path()
            pdf_filename = os.path.basename(pdf_path)
            
            # 기존 데이터 로드
            if os.path.exists(mask_file):
                with open(mask_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'files': []
                }
            
            # MaskEntry를 딕셔너리로 변환
            masks_data = []
            for mask in masks:
                masks_data.append({
                    'page_index': mask.page_index,
                    'rect': {
                        'x0': mask.rect.x0,
                        'y0': mask.rect.y0,
                        'x1': mask.rect.x1,
                        'y1': mask.rect.y1,
                    },
                    'note': mask.note,
                })
            
            # 파일별 데이터 구성
            file_data = {
                'pdf_file': pdf_filename,
                'saved_at': datetime.now().isoformat(),
                'mask_count': len(masks),
                'masks': masks_data,
            }
            
            # 기존 파일 데이터가 있으면 업데이트, 없으면 추가
            file_found = False
            for i, file_entry in enumerate(data['files']):
                if file_entry['pdf_file'] == pdf_filename:
                    data['files'][i] = file_data
                    file_found = True
                    break
            
            if not file_found:
                data['files'].append(file_data)
            
            # JSON으로 저장
            with open(mask_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True, mask_file
            
        except Exception as e:
            return False, f"마스킹 데이터 저장 실패: {str(e)}"
    
    def load_masks(self, pdf_path: str) -> Tuple[bool, List[MaskEntry], str]:
        """
        일자별 JSON 파일에서 특정 PDF의 마스킹 데이터 로드
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            Tuple[bool, List[MaskEntry], str]: (성공 여부, 마스킹 리스트, 메시지)
        """
        try:
            mask_file = self.get_mask_file_path()
            pdf_filename = os.path.basename(pdf_path)
            
            if not os.path.exists(mask_file):
                return True, [], "오늘 날짜의 마스킹 데이터 없음"
            
            with open(mask_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 해당 PDF 파일의 데이터 찾기
            file_data = None
            for file_entry in data.get('files', []):
                if file_entry['pdf_file'] == pdf_filename:
                    file_data = file_entry
                    break
            
            if not file_data:
                return True, [], f"{pdf_filename}의 마스킹 데이터 없음"
            
            # 딕셔너리를 MaskEntry로 변환
            masks = []
            for mask_data in file_data.get('masks', []):
                rect_data = mask_data['rect']
                rect = fitz.Rect(
                    rect_data['x0'],
                    rect_data['y0'],
                    rect_data['x1'],
                    rect_data['y1']
                )
                mask = MaskEntry(
                    page_index=mask_data['page_index'],
                    rect=rect,
                    note=mask_data.get('note', '')
                )
                masks.append(mask)
            
            return True, masks, f"{len(masks)}개의 마스킹 데이터 로드 완료"
            
        except Exception as e:
            return False, [], f"마스킹 데이터 로드 실패: {str(e)}"
    
    def delete_masks(self, pdf_path: str) -> Tuple[bool, str]:
        """
        일자별 JSON 파일에서 특정 PDF의 마스킹 데이터 삭제
        
        Args:
            pdf_path: PDF 파일 경로
            
        Returns:
            Tuple[bool, str]: (성공 여부, 메시지)
        """
        try:
            mask_file = self.get_mask_file_path()
            pdf_filename = os.path.basename(pdf_path)
            
            if not os.path.exists(mask_file):
                return True, "마스킹 데이터 파일 없음"
            
            with open(mask_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 해당 PDF 파일 데이터 제거
            original_count = len(data.get('files', []))
            data['files'] = [f for f in data.get('files', []) if f['pdf_file'] != pdf_filename]
            
            if len(data['files']) < original_count:
                # 데이터 저장
                with open(mask_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                return True, "마스킹 데이터 삭제 완료"
            else:
                return True, "해당 파일의 마스킹 데이터 없음"
                
        except Exception as e:
            return False, f"마스킹 데이터 삭제 실패: {str(e)}"

