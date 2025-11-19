"""
다이얼로그 UI 컴포넌트
"""

from typing import Optional
from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QProgressDialog,
    QApplication,
)
from PyQt6.QtCore import Qt

from ..managers.license_manager import LicenseManager


class SerialInputDialog(QDialog):
    """
    시리얼 번호 입력 다이얼로그
    
    라이선스 인증을 위한 시리얼 번호를 입력받습니다.
    """
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        초기화
        
        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.license_manager = LicenseManager()
        self.init_ui()
    
    def init_ui(self) -> None:
        """UI 초기화"""
        self.setWindowTitle("라이선스 인증")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        # 안내 문구
        info_label = QLabel(
            "프로그램을 사용하려면 시리얼 번호를 입력해주세요.\n\n"
            "형식: XXXX-XXXX-XXXX-XXXX"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 시리얼 번호 입력
        self.serial_input = QLineEdit()
        self.serial_input.setPlaceholderText("시리얼 번호 입력")
        self.serial_input.setMaxLength(19)  # XXXX-XXXX-XXXX-XXXX
        layout.addWidget(self.serial_input)
        
        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        # 인증 버튼
        self.activate_button = QPushButton("인증")
        self.activate_button.clicked.connect(self.activate)
        button_layout.addWidget(self.activate_button)
        
        # 취소 버튼
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        # 상태 메시지
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def activate(self) -> None:
        """인증 버튼 클릭"""
        serial = self.serial_input.text().strip()
        
        if not serial:
            self.status_label.setText("시리얼 번호를 입력해주세요.")
            return
        
        # 진행 다이얼로그 표시
        progress = QProgressDialog("라이선스 서버에 연결 중...", None, 0, 0, self)
        progress.setWindowTitle("인증 중")
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()
        QApplication.processEvents()
        
        # 라이선스 활성화 시도
        success, message = self.license_manager.activate_license(serial)
        
        progress.close()
        
        if success:
            QMessageBox.information(
                self,
                "인증 성공",
                "라이선스가 성공적으로 활성화되었습니다."
            )
            self.accept()
        else:
            self.status_label.setText(message)
            QMessageBox.warning(
                self,
                "인증 실패",
                message
            )

