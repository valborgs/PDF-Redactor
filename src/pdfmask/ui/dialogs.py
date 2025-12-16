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


class PasswordInputDialog(QDialog):
    """
    PDF 암호 입력 다이얼로그
    
    암호화된 PDF 파일을 열기 위한 암호를 입력받습니다.
    """
    
    def __init__(self, file_path: str, error_message: str = "", parent: Optional[QWidget] = None) -> None:
        """
        초기화
        
        Args:
            file_path: PDF 파일 경로
            error_message: 이전 시도에서 발생한 오류 메시지 (선택)
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.file_path = file_path
        self.error_message = error_message
        self.password = ""
        self.init_ui()
    
    def init_ui(self) -> None:
        """UI 초기화"""
        self.setWindowTitle("PDF 암호 입력")
        self.setModal(True)
        self.setFixedSize(400, 180)
        
        layout = QVBoxLayout()
        
        # 파일명 표시
        import os
        filename = os.path.basename(self.file_path)
        file_label = QLabel(f"<b>{filename}</b>")
        file_label.setWordWrap(True)
        layout.addWidget(file_label)
        
        # 안내 문구
        info_label = QLabel("이 PDF 파일은 암호로 보호되어 있습니다.\n암호를 입력해주세요.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 암호 입력
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("암호 입력")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.accept_password)
        layout.addWidget(self.password_input)
        
        # 오류 메시지 (이전 시도 실패 시)
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")
        if self.error_message:
            self.status_label.setText(self.error_message)
        layout.addWidget(self.status_label)
        
        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        # 확인 버튼
        self.ok_button = QPushButton("확인")
        self.ok_button.clicked.connect(self.accept_password)
        button_layout.addWidget(self.ok_button)
        
        # 취소 버튼
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 암호 입력창에 포커스
        self.password_input.setFocus()
    
    def accept_password(self) -> None:
        """확인 버튼 클릭"""
        password = self.password_input.text()
        
        if not password:
            self.status_label.setText("암호를 입력해주세요.")
            return
        
        self.password = password
        self.accept()
    
    def get_password(self) -> str:
        """입력된 암호 반환"""
        return self.password
