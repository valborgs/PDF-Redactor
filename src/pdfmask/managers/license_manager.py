"""
라이선스 관리 모듈
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Tuple


class LicenseManager:
    """
    라이선스 인증 및 관리 클래스
    
    시리얼 번호 기반 라이선스 인증을 처리합니다.
    """
    
    def __init__(self) -> None:
        """
        초기화
        
        프로젝트 루트 경로에 .license 파일을 생성/관리합니다.
        """
        # 프로젝트 루트 경로 (src/pdfmask/managers/ -> src/ -> project_root/)
        current_file = os.path.abspath(__file__)
        managers_dir = os.path.dirname(current_file)  # managers/
        pdfmask_dir = os.path.dirname(managers_dir)   # pdfmask/
        src_dir = os.path.dirname(pdfmask_dir)        # src/
        self.project_root = os.path.dirname(src_dir)  # project_root/
        self.license_file = os.path.join(self.project_root, ".license")
    
    def is_licensed(self) -> bool:
        """
        라이선스가 유효한지 확인
        
        Returns:
            bool: 라이선스 유효 여부
        """
        if not os.path.exists(self.license_file):
            return False
        
        try:
            with open(self.license_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('activated', False)
        except Exception:
            return False
    
    def validate_serial(self, serial: str) -> Tuple[bool, str]:
        """
        시리얼 번호 형식 검증 (로컬 검증)
        
        Args:
            serial: 입력된 시리얼 번호
            
        Returns:
            Tuple[bool, str]: (검증 성공 여부, 메시지)
        """
        # 시리얼 번호 형식 검증 (예: XXXX-XXXX-XXXX-XXXX)
        serial = serial.strip().upper()
        
        if len(serial) == 0:
            return False, "시리얼 번호를 입력해주세요."
        
        # 간단한 형식 검증
        parts = serial.split('-')
        if len(parts) != 4:
            return False, "올바른 형식이 아닙니다. (XXXX-XXXX-XXXX-XXXX)"
        
        for part in parts:
            if len(part) != 4:
                return False, "올바른 형식이 아닙니다. (XXXX-XXXX-XXXX-XXXX)"
        
        return True, "형식 검증 성공"
    
    def activate_license(self, serial: str) -> Tuple[bool, str]:
        """
        라이선스 활성화 (서버 인증 시뮬레이션)
        
        실제 구현에서는 여기서 서버 API를 호출해야 합니다.
        현재는 로컬에서 간단한 검증만 수행합니다.
        
        Args:
            serial: 시리얼 번호
            
        Returns:
            Tuple[bool, str]: (활성화 성공 여부, 메시지)
        """
        # 1. 형식 검증
        valid, msg = self.validate_serial(serial)
        if not valid:
            return False, msg
        
        # 2. 서버 인증 시뮬레이션
        # 실제 구현: requests.post('https://license-server.com/activate', ...)
        
        # 간단한 해시 기반 검증 (예시)
        serial_hash = hashlib.sha256(serial.encode()).hexdigest()
        
        # 테스트용 시리얼: TEST-1234-5678-ABCD
        valid_serials = [
            "TEST-1234-5678-ABCD",
            "DEMO-0000-0000-0001",
        ]
        
        if serial not in valid_serials:
            return False, "유효하지 않은 시리얼 번호입니다."
        
        # 3. 라이선스 파일 저장
        try:
            license_data = {
                'activated': True,
                'serial': serial,
                'serial_hash': serial_hash,
                'activated_at': datetime.now().isoformat(),
            }
            
            with open(self.license_file, 'w', encoding='utf-8') as f:
                json.dump(license_data, f, indent=2, ensure_ascii=False)
            
            return True, "라이선스 활성화 완료"
            
        except Exception as e:
            return False, f"라이선스 저장 실패: {str(e)}"
    
    def deactivate_license(self) -> None:
        """
        라이선스 비활성화
        
        .license 파일을 삭제합니다.
        """
        if os.path.exists(self.license_file):
            try:
                os.remove(self.license_file)
            except Exception:
                pass

