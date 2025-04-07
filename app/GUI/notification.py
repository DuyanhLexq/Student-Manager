from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QApplication,QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect,QPoint,pyqtProperty,QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette,QPixmap


class FloatingNotification(QWidget):
    def __init__(self, message, parent=None, bg_color="#28a745", icon_path=None, duration=3000):
        super().__init__(parent)
        self.parent_widget = parent
        self.opacity = 1.0
        self.duration = duration

        # Cờ và hiệu ứng
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        # Giao diện
        self.setFixedHeight(60)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 10px;
            }}
        """)

        # Layout chính
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)

        # Icon
        if icon_path:
            icon_label = QLabel()
            pixmap = QPixmap(icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            layout.addWidget(icon_label)

        # Nội dung
        self.message_label = QLabel(message)
        self.message_label.setStyleSheet("color: white;")
        self.message_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(self.message_label)

        # Hẹn giờ tự đóng
        QTimer.singleShot(self.duration, self.fade_out)

    def show_bottom_center(self):
        if self.parent_widget:
            self.parent_widget.installEventFilter(self)
            self.update_position()
        self.show()

    def update_position(self):
        parent_pos = self.parent_widget.mapToGlobal(QPoint(0, 0))
        parent_size = self.parent_widget.size()
        parent_geom = self.parent_widget.geometry()
        notif_width = self.width()  # Lấy chiều rộng của thông báo
        notif_height = self.height()  # Lấy chiều cao của thông báo
        x = parent_geom.x() + (parent_geom.width() - notif_width) // 2
        y = parent_geom.y() + parent_geom.height() - notif_height - 30
        self.move(x, y)

    # Bắt sự kiện khi cửa sổ chính di chuyển
    def eventFilter(self, obj, event):
        if obj == self.parent_widget and event.type() == event.Move:
            self.update_position()
        return super().eventFilter(obj, event)

    # Fade animation
    def fade_out(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.finished.connect(self.close)
        self.anim.start()

    def get_opacity(self):
        return QWidget.windowOpacity(self)

    def set_opacity(self, value):
        QWidget.setWindowOpacity(self, value)

    windowOpacity = pyqtProperty(float, fget=get_opacity, fset=set_opacity)