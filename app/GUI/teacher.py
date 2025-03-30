from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class TeacherPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        label = QLabel("Quản lý Giáo viên")
        label.setFont(QFont("Arial", 24))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addStretch()
