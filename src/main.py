"""
PDF Mask - 메인 실행 파일
PyQt6 기반 PDF 마스킹 애플리케이션
"""

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox

from pdfmask.managers import LicenseManager, LogManager
from pdfmask.ui import MainWindow, SerialInputDialog


def main() -> None:
    """
    메인 함수
    
    라이선스 검증 후 메인 윈도우를 표시합니다.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("PDF Mask")
    
    # 임시 로그 관리자 (라이선스 인증용)
    temp_log = LogManager()
    
    # 라이선스 확인
    license_manager = LicenseManager()
    
    if not license_manager.is_licensed():
        # 라이선스가 없으면 시리얼 번호 입력 다이얼로그 표시
        temp_log.log_license_check(False, "No license file found")
        serial_dialog = SerialInputDialog()
        result = serial_dialog.exec()
        
        if result != QDialog.DialogCode.Accepted:
            # 사용자가 취소하면 프로그램 종료
            temp_log.log_license_check(False, "User cancelled license activation")
            QMessageBox.warning(
                None,
                "종료",
                "라이선스 인증이 필요합니다.\n프로그램을 종료합니다."
            )
            sys.exit(0)
        else:
            temp_log.log_license_check(True, "License activated successfully")
    else:
        temp_log.log_license_check(True, "License verified")
    
    # 메인 윈도우 표시
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

