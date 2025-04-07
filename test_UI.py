from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QApplication
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect
from PyQt5.QtGui import QFont, QColor, QPalette


class FloatingNotification(QWidget):
    def __init__(self, message, parent=None, duration=3000):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(300, 80)

        # Nội dung hiển thị
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)

        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setFont(QFont("Segoe UI", 10))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)

        # Style đẹp kiểu web
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 200);
                border-radius: 12px;
            }
        """)

        # Animation fade in
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

        # Tự động đóng sau duration ms
        QTimer.singleShot(duration, self.fade_out)

    def show_in_corner(self, parent_widget=None):
        if parent_widget:
            parent_rect = parent_widget.geometry()
            x = parent_rect.x() + parent_rect.width() - self.width() - 20
            y = parent_rect.y() + 20
        else:
            screen = QApplication.desktop().availableGeometry()
            x = screen.width() - self.width() - 20
            y = 20
        self.move(x, y)
        self.show()

    def fade_out(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)
        self.animation.start()
