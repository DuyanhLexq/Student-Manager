# File: teacher.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.addTeacher_func import AddTeacherPage

class TeacherPage(QWidget):
    def __init__(self, main_stack=None):
        super().__init__()
        self.main_stack = main_stack
        self.initUI()
        self.applyStyles()
    
    def initUI(self):
        self.sample_data = [
            ["GV001", "Nguyễn Văn A", "01/01/1980", "2010"],
            ["GV002", "Trần Thị B", "05/03/1985", "2012"],
            ["GV003", "Lê Văn C", "12/07/1978", "2008"]
        ]
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20,20,20,20)
        main_layout.setSpacing(15)
        
        # Phần tìm kiếm
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm giáo viên theo tên...")
        self.search_input.setFixedHeight(30)
        name_list = [data[1] for data in self.sample_data]
        completer = QCompleter(name_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_input.setCompleter(completer)
        self.search_input.returnPressed.connect(self.search_teacher)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        
        # Nút chức năng: Thêm, Sửa, Xóa, Biểu đồ
        func_layout = QHBoxLayout()
        self.add_button = QPushButton("Thêm")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        self.chart_button = QPushButton("Biểu đồ")
        for btn in [self.add_button, self.edit_button, self.delete_button, self.chart_button]:
            btn.setFixedHeight(30)
            btn.setFont(QFont("Arial", 12))
            func_layout.addWidget(btn)
        main_layout.addLayout(func_layout)
        
        # Bảng danh sách giáo viên
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Chọn", "ID", "Tên giáo viên", "Ngày sinh", "Năm vào làm việc"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setRowCount(len(self.sample_data))
        for row, data in enumerate(self.sample_data):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, checkbox_item)
            for col, item in enumerate(data):
                self.table.setItem(row, col+1, QTableWidgetItem(item))
        main_layout.addWidget(self.table)
        
        # Kết nối sự kiện
        self.add_button.clicked.connect(self.go_to_add_teacher)
        self.edit_button.clicked.connect(self.edit_teacher)
        self.delete_button.clicked.connect(self.delete_teacher)
        self.chart_button.clicked.connect(self.show_chart)
    
    def applyStyles(self):
        style = """
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
            btn.setStyleSheet(style)
    
    def search_teacher(self):
        query = self.search_input.text().strip()
        print(f"Tìm kiếm giáo viên theo tên: {query}")
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 2)
            if query.lower() in item.text().lower():
                self.table.showRow(row)
            else:
                self.table.hideRow(row)
    
    def go_to_add_teacher(self):
        print("Chuyển sang trang thêm giáo viên")
        if self.main_stack:
            add_page = AddTeacherPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
        else:
            print("Main stack chưa được cung cấp!")
    
    def edit_teacher(self):
        print("Sửa thông tin giáo viên")
    
    def delete_teacher(self):
        print("Xóa giáo viên")
    
    def show_chart(self):
        print("Hiển thị biểu đồ giáo viên")
