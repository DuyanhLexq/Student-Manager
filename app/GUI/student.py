from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter, QDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.addStudent_func import AddStudentPage  # Import widget thêm học sinh
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime

class ChartWindow(QDialog):
    def __init__(self, student_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Biểu đồ thống kê")
        self.resize(800, 600)
        self.student_data = student_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.figure, (self.ax_gender, self.ax_age) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.plot_charts()

    def plot_charts(self):
        genders = {"Nam": 0, "Nữ": 0}
        ages = []
        current_year = datetime.datetime.now().year

        for data in self.student_data:
            gender = data[2].strip()
            dob_str = data[3].strip()  # định dạng dd/mm/yyyy
            try:
                day, month, year = map(int, dob_str.split("/"))
                age = current_year - year
                ages.append(age)
            except Exception as e:
                print("Lỗi chuyển đổi ngày sinh:", e)
                continue

            if gender in genders:
                genders[gender] += 1

        self.ax_gender.clear()
        self.ax_gender.bar(genders.keys(), genders.values(), color=['#3498db','#e74c3c'])
        self.ax_gender.set_title("Số lượng Nam/Nữ")
        self.ax_gender.set_ylabel("Số lượng")

        self.ax_age.clear()
        if ages:
            self.ax_age.hist(ages, bins=range(min(ages), max(ages) + 2), color='#2ecc71', edgecolor='black')
            self.ax_age.set_title("Phân bố độ tuổi")
            self.ax_age.set_xlabel("Độ tuổi")
            self.ax_age.set_ylabel("Số lượng")
        else:
            self.ax_age.text(0.5, 0.5, "Không có dữ liệu", horizontalalignment='center')
        self.canvas.draw()

class StudentPage(QWidget):
    def __init__(self, main_stack=None):
        """
        main_stack: QStackedWidget chứa các trang của ứng dụng, dùng để chuyển trang.
        """
        super().__init__()
        self.main_stack = main_stack
        self.initUI()
        self.applyStyles()

    def initUI(self):
        self.sample_data = [
            ["HS001", "Nguyễn Văn A", "Nam", "15/03/2005"],
            ["HS002", "Trần Thị B", "Nữ", "20/07/2006"],
            ["HS003", "Lê Văn C", "Nam", "05/12/2005"],
            ["HS004", "Phạm Thị D", "Nữ", "25/09/2004"]
        ]
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Phần tìm kiếm (đặt lên đầu)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm học sinh theo tên...")
        self.search_input.setFixedHeight(30)
        name_list = [data[1] for data in self.sample_data]
        completer = QCompleter(name_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_input.setCompleter(completer)
        self.search_input.returnPressed.connect(self.search_student)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Nút chức năng: Thêm, Sửa, Xóa, Biểu đồ
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

        # Bảng danh sách học sinh với cột "Chọn"
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Chọn", "ID", "Tên", "Giới tính", "Ngày sinh"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setRowCount(len(self.sample_data))
        for row, data in enumerate(self.sample_data):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, checkbox_item)
            for col, item in enumerate(data):
                self.table.setItem(row, col + 1, QTableWidgetItem(item))
        main_layout.addWidget(self.table)

        # Kết nối sự kiện
        self.add_button.clicked.connect(self.go_to_add_student)
        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)
        self.chart_button.clicked.connect(self.show_chart)

    def applyStyles(self):
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
        query = self.search_input.text().strip()
        print(f"Tìm kiếm học sinh theo tên: {query}")
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 2)
            if query.lower() in item.text().lower():
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def go_to_add_student(self):
        print("Chuyển sang trang thêm học sinh")
        if self.main_stack:
            add_page = AddStudentPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
        else:
            print("Main stack chưa được cung cấp!")
    
    def edit_student(self):
        print("Sửa thông tin học sinh")
    
    def delete_student(self):
        print("Xóa học sinh")
    
    def show_chart(self):
        row_count = self.table.rowCount()
        student_data = []
        for row in range(row_count):
            if not self.table.isRowHidden(row):
                row_data = []
                for col in range(1, self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                student_data.append(row_data)
        chart_win = ChartWindow(student_data, self)
        chart_win.exec_()

