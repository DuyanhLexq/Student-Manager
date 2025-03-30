from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        # Thiết lập margin để chữ sát lề trên, bên phải
        layout.setContentsMargins(20, 10, 20, 20)
        self.hello_label = QLabel("Hello user")
        self.hello_label.setFont(QFont("Arial", 24))
        self.hello_label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        layout.addWidget(self.hello_label)
        layout.addStretch()
