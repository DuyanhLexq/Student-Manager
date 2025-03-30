from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class StudentPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.applyStyles()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # --- Phần tìm kiếm học sinh (đặt lên đầu) ---
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm học sinh...")
        self.search_input.setFixedHeight(30)
        search_button = QPushButton("Tìm kiếm")
        search_button.setFixedHeight(30)
        search_button.setFont(QFont("Arial", 12))
        search_button.clicked.connect(self.search_student)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # --- Phần các nút chức năng: Thêm, Sửa, Xóa, Biểu đồ ---
        func_button_layout = QHBoxLayout()
        self.add_button = QPushButton("Thêm")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        self.chart_button = QPushButton("Biểu đồ")
        for btn in [self.add_button, self.edit_button, self.delete_button, self.chart_button]:
            btn.setFixedHeight(30)
            btn.setFont(QFont("Arial", 12))
            func_button_layout.addWidget(btn)
        main_layout.addLayout(func_button_layout)

        # --- Bảng danh sách học sinh (đặt xuống dưới) ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Tên", "Lớp", "Điểm"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Dữ liệu mẫu
        sample_data = [
            ["HS001", "Nguyễn Văn A", "10A1", "8.5"],
            ["HS002", "Trần Thị B", "10A2", "9.0"],
            ["HS003", "Lê Văn C", "10A3", "7.5"]
        ]
        self.table.setRowCount(len(sample_data))
        for row, data in enumerate(sample_data):
            for col, item in enumerate(data):
                self.table.setItem(row, col, QTableWidgetItem(item))
        main_layout.addWidget(self.table)

        # --- Kết nối sự kiện ---
        self.add_button.clicked.connect(self.add_student)
        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.chart_button.clicked.connect(self.show_chart)

    def applyStyles(self):
        # QSS cho các nút: không hiện border mặc định,
        # Khi ấn hoặc focus hiển thị nền hộp xám và gạch chân chữ.
        button_style = """
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:pressed, QPushButton:focus {
                background-color: #d3d3d3;
                text-decoration: underline;
            }
        """
        for btn in [self.add_button, self.edit_button, self.delete_button, self.chart_button]:
            btn.setStyleSheet(button_style)

    def search_student(self):
        query = self.search_input.text()
        print(f"Tìm kiếm học sinh: {query}")

    def add_student(self):
        print("Thêm học sinh")

    def edit_student(self):
        print("Sửa thông tin học sinh")

    def delete_student(self):
        print("Xóa học sinh")

    def show_chart(self):
        print("Hiển thị biểu đồ")
