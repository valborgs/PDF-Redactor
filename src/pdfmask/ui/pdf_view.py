"""
PDF 뷰어 UI 컴포넌트
"""

from typing import Optional
from PyQt6.QtWidgets import QWidget, QScrollArea
from PyQt6.QtCore import Qt, QPoint, QRect, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
import fitz


class PdfPageView(QWidget):
    """
    PDF 페이지를 표시하고 마스킹 영역을 선택할 수 있는 커스텀 위젯
    
    Ctrl + 드래그로 마스킹 영역을 선택합니다.
    """
    
    # 시그널: (page_index, fitz.Rect)
    maskCreated = pyqtSignal(int, object)
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        초기화
        
        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        
        # 페이지 표시 관련
        self._pixmap: Optional[QPixmap] = None
        self._page_index: int = 0
        self._page_width: float = 0.0
        self._page_height: float = 0.0
        
        # 마스킹 드래그 관련
        self._start_pos: Optional[QPoint] = None
        self._current_rect: Optional[QRect] = None
        self._ctrl_pressed_during_drag: bool = False
        
        # 저장된 마스킹 영역들 (화면 좌표)
        self._saved_masks: list[QRect] = []
        
        # 줌 레벨
        self._zoom_level: float = 1.0  # 100%
        
        # 배경 스타일 (PDF 영역은 흰색)
        self.setStyleSheet("background-color: #ffffff;")
        self.setMinimumSize(400, 300)
        
    def set_page(
        self, 
        page_index: int, 
        pixmap: QPixmap, 
        page_width: float, 
        page_height: float,
        masks: list = None
    ) -> None:
        """
        페이지 정보 설정
        
        Args:
            page_index: 페이지 인덱스 (0-based)
            pixmap: 렌더링된 페이지 이미지
            page_width: PDF 페이지 실제 너비
            page_height: PDF 페이지 실제 높이
            masks: 저장된 마스킹 정보 리스트
        """
        self._page_index = page_index
        self._pixmap = pixmap
        self._page_width = page_width
        self._page_height = page_height
        
        # 저장된 마스킹 영역 표시를 위해 변환
        self._saved_masks = []
        if masks and pixmap:
            for mask in masks:
                if mask.page_index == page_index:
                    # PDF 좌표를 화면 좌표로 변환
                    screen_rect = self._convert_to_screen_rect(mask.rect)
                    if screen_rect:
                        self._saved_masks.append(screen_rect)
        
        # 위젯 크기를 pixmap 크기에 맞춤
        if pixmap is not None:
            self.setFixedSize(pixmap.size())
        
        self.update()
    
    def set_zoom_level(self, zoom: float) -> None:
        """
        줌 레벨 설정
        
        Args:
            zoom: 줌 레벨 (1.0 = 100%)
        """
        self._zoom_level = zoom
    
    def clear(self) -> None:
        """화면 초기화"""
        self._pixmap = None
        self._page_index = 0
        self._page_width = 0.0
        self._page_height = 0.0
        self._saved_masks = []
        self._start_pos = None
        self._current_rect = None
        self._ctrl_pressed_during_drag = False
        self.setMinimumSize(400, 300)
        self.update()
    
    def paintEvent(self, event) -> None:
        """페이지 렌더링"""
        painter = QPainter(self)
        
        # Pixmap 그리기
        if self._pixmap is not None:
            painter.drawPixmap(0, 0, self._pixmap)
        
        # 저장된 마스킹 영역 그리기 (반투명 빨간색)
        if self._saved_masks:
            brush = QBrush(QColor(255, 0, 0, 60))
            painter.setBrush(brush)
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            
            for rect in self._saved_masks:
                painter.drawRect(rect)
        
        # 드래그 중인 사각형 그리기 (반투명 파란색)
        if self._current_rect is not None:
            brush = QBrush(QColor(0, 120, 255, 80))
            painter.setBrush(brush)
            pen = QPen(QColor(0, 120, 255), 2)
            painter.setPen(pen)
            
            painter.drawRect(self._current_rect)
        
        painter.end()
    
    def mousePressEvent(self, event) -> None:
        """마우스 클릭 시작"""
        # Ctrl + 좌클릭인 경우만 드래그 시작
        if (event.button() == Qt.MouseButton.LeftButton and 
            event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            
            self._start_pos = event.pos()
            self._current_rect = None
            self._ctrl_pressed_during_drag = True
    
    def mouseMoveEvent(self, event) -> None:
        """마우스 드래그 중"""
        if self._ctrl_pressed_during_drag and self._start_pos is not None:
            # 시작점과 현재점으로 사각형 생성
            current_pos = event.pos()
            
            # QRect 생성 (좌상단, 우하단을 자동으로 정규화)
            self._current_rect = QRect(self._start_pos, current_pos).normalized()
            
            # 화면 업데이트
            self.update()
    
    def mouseReleaseEvent(self, event) -> None:
        """마우스 클릭 종료"""
        if (self._ctrl_pressed_during_drag and 
            self._start_pos is not None and 
            self._current_rect is not None):
            
            # 화면 좌표를 PDF 페이지 좌표로 변환
            pdf_rect = self._convert_to_pdf_rect(self._current_rect)
            
            if pdf_rect is not None:
                # 시그널 발생
                self.maskCreated.emit(self._page_index, pdf_rect)
                
                # 저장된 마스킹 목록에 추가 (화면에 즉시 표시)
                self._saved_masks.append(self._current_rect)
            
            # 상태 초기화
            self._start_pos = None
            self._current_rect = None
            self._ctrl_pressed_during_drag = False
            
            # 화면 업데이트
            self.update()

    def wheelEvent(self, event) -> None:
        """마우스 휠 이벤트 (Ctrl + 휠로 줌)"""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # Ctrl이 눌린 상태에서는 확대/축소만 처리
            delta = event.angleDelta().y()
            # QScrollArea.setWidget()으로 추가된 위젯의 parent()는 viewport이므로
            # window()를 사용하여 MainWindow를 찾아 확대/축소 호출
            main_window = self.window()
            if delta > 0:
                if main_window is not None and hasattr(main_window, "zoom_in"):
                    main_window.zoom_in()
            else:
                if main_window is not None and hasattr(main_window, "zoom_out"):
                    main_window.zoom_out()
            event.accept()
        else:
            # Ctrl이 아닐 때는 기본 스크롤 동작 유지
            super().wheelEvent(event)
    
    def _convert_to_pdf_rect(self, screen_rect: QRect) -> Optional[fitz.Rect]:
        """
        화면 좌표를 PDF 페이지 좌표로 변환
        
        Args:
            screen_rect: 화면 좌표 사각형
            
        Returns:
            Optional[fitz.Rect]: PDF 좌표 사각형 또는 None
        """
        if self._pixmap is None or self._page_width == 0 or self._page_height == 0:
            return None
        
        # 스케일 비율 계산
        scale_x = self._page_width / self._pixmap.width()
        scale_y = self._page_height / self._pixmap.height()
        
        # 화면 좌표를 PDF 좌표로 변환
        x0 = screen_rect.left() * scale_x
        y0 = screen_rect.top() * scale_y
        x1 = screen_rect.right() * scale_x
        y1 = screen_rect.bottom() * scale_y
        
        # fitz.Rect 생성 (x0, y0, x1, y1)
        return fitz.Rect(x0, y0, x1, y1)
    
    def _convert_to_screen_rect(self, pdf_rect: fitz.Rect) -> Optional[QRect]:
        """
        PDF 좌표를 화면 좌표로 변환
        
        Args:
            pdf_rect: PDF 좌표 사각형
            
        Returns:
            Optional[QRect]: 화면 좌표 사각형 또는 None
        """
        if self._pixmap is None or self._page_width == 0 or self._page_height == 0:
            return None
        
        # 스케일 비율 계산
        scale_x = self._pixmap.width() / self._page_width
        scale_y = self._pixmap.height() / self._page_height
        
        # PDF 좌표를 화면 좌표로 변환
        x0 = int(pdf_rect.x0 * scale_x)
        y0 = int(pdf_rect.y0 * scale_y)
        x1 = int(pdf_rect.x1 * scale_x)
        y1 = int(pdf_rect.y1 * scale_y)
        
        return QRect(QPoint(x0, y0), QPoint(x1, y1))


class ScrollablePdfView(QScrollArea):
    """
    스크롤 가능한 PDF 뷰 컨테이너
    
    PdfPageView를 감싸서 스크롤 기능을 제공합니다.
    """
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """
        초기화
        
        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        
        # PDF 뷰 위젯
        self.pdf_view = PdfPageView(self)
        self.setWidget(self.pdf_view)
        
        # 스크롤 설정
        self.setWidgetResizable(False)  # 위젯 크기 자동 조절 끄기
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # 크기 정책 설정
        self.setMinimumWidth(400)
        
        # PDF를 가운데 정렬
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 배경색 설정 (회색)
        self.setStyleSheet("QScrollArea { background-color: #808080; }")
        
        # 줌 레벨
        self.zoom_level: float = 1.0  # 100%
        self.min_zoom: float = 0.5  # 최소 50%
        self.max_zoom: float = 2.0  # 최대 200%
        
    def zoom_in(self) -> None:
        """줌 인 (10% 증가)"""
        if self.zoom_level < self.max_zoom:
            self.zoom_level = min(self.zoom_level + 0.1, self.max_zoom)
            main_window = self.window()
            if main_window is not None and hasattr(main_window, 'update_page_view'):
                main_window.update_page_view()
    
    def zoom_out(self) -> None:
        """줌 아웃 (10% 감소)"""
        if self.zoom_level > self.min_zoom:
            self.zoom_level = max(self.zoom_level - 0.1, self.min_zoom)
            main_window = self.window()
            if main_window is not None and hasattr(main_window, 'update_page_view'):
                main_window.update_page_view()

    def wheelEvent(self, event) -> None:
        """마우스 휠 이벤트 (Ctrl + 휠로 줌)"""
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            # 기본 스크롤 동작 유지
            super().wheelEvent(event)

