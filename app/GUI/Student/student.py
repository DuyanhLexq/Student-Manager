from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter, QDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.Student.addStudent_func import AddStudentPage  # Import widget thêm học sinh
from GUI.util import formPage
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

class StudentPage(formPage):
    def __init__(self, main_stack=None):
        """
        main_stack: QStackedWidget chứa các trang của ứng dụng, dùng để chuyển trang.
        """
        self.main_stack = main_stack
        super().__init__(
            [
            ["HS001", "Nguyễn Văn A", "Nam", "15/03/2005"],
            ["HS002", "Trần Thị B", "Nữ", "20/07/2006"],
            ["HS003", "Lê Văn C", "Nam", "05/12/2005"],
            ["HS004", "Phạm Thị D", "Nữ", "25/09/2004"]
        ],
        field= ["Chọn", "ID", "Tên", "Giới tính", "Ngày sinh"],
        title= "Quản lý học sinh",
        main_stack= self.main_stack,
        search_text = "Tìm kiếm học sinh",
        filter_fields = ["ID", "Tên", "Giới tính", "Ngày sinh"]
        )

    
    def go_to_add_page(self):
        if self.main_stack:
            add_page = AddStudentPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
        else:
            print("Main stack chưa được cung cấp!")

class GradesPage(formPage):
    def __init__(self, main_stack=None):
        """
        main_stack: QStackedWidget chứa các trang của ứng dụng, dùng để chuyển trang.
        """
        self.main_stack = main_stack
        super().__init__(
            [
            ["HS001", "Nguyễn Văn A", "10"],
            ["HS002", "Trần Thị B", "10"],
            ["HS003", "Lê Văn C", "10"],
            ["HS004", "Phạm Thị D", "10"]
        ],
        field= ["Chọn", "ID", "Tên", "Điểm"],
        title= "Quản lý điểm",
        main_stack =  self.main_stack,
        search_text = "Tìm kiếm học sinh",
        filter_fields = ["ID", "Tên", "Điểm"]
        )

class TuitionPage(formPage):
    def __init__(self, main_stack = None):
        self.main_stack = main_stack
        super().__init__(
            [
            ["HS001", "Nguyễn Văn A", "10.000.000","Đã đóng"],
            ["HS002", "Trần Thị B", "10.000.000","Chưa đóng"],
            ["HS003", "Lê Văn C", "10.000.000","Đã đóng"],
            ["HS004", "Phạm Thị D", "10.000.000","Chưa đóng"]
        ],
        field= ["Chọn", "ID", "Tên", "Học phí","Đóng"],
        title= "Quản lý học phí",
        main_stack= self.main_stack,
        search_text = "Tìm kiếm học sinh",
        filter_fields= ["ID", "Tên", "Học phí"],
        )
