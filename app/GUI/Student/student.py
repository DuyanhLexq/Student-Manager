from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter, QDialog,QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.Student.addStudent_func import AddStudentPage  # Import widget thêm học sinh
from GUI.util import formPage
from GUI.util import formPage,get_right_table_data_form
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from functions.functions import get_preview_data
from sqlQuery import GET_PREVIEW_STUDENT_DATA_QUERY,GET_GRADES_DATA_QUERY,GET_TUITION_DATA_QUERY
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
        self.preview_data = get_right_table_data_form(get_preview_data(GET_PREVIEW_STUDENT_DATA_QUERY))
        super().__init__(
            self.preview_data,
            field=["Chọn", "ID", "Tên", "Giới tính", "Ngày sinh"],
            title="Quản lý học sinh",
            main_stack=self.main_stack,
            search_text="Tìm kiếm học sinh",
            filter_fields=["ID", "Tên", "Giới tính", "Ngày sinh"]
        )
    
    def delete_student(self):
        """
        Ghi đè phương thức xóa học sinh để hiển thị hộp thoại xác nhận với thông báo:
        - Nếu chỉ chọn 1 học sinh: "Xác nhận xóa học sinh [ID]- [Tên]?"
        - Nếu chọn nhiều học sinh: liệt kê thông tin của các học sinh cần xóa.
        """
        selected_students = []
        # Duyệt qua các dòng của bảng để lấy những dòng có checkbox được tích
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                # Lấy thông tin ID (cột 1) và Tên (cột 2)
                student_id = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
                student_name = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
                selected_students.append((row, student_id, student_name))
        
        if not selected_students:
            QMessageBox.information(self, "Thông báo", "Chưa chọn học sinh nào để xóa.")
            return
        
        # Tạo thông báo xác nhận dựa trên số lượng học sinh được chọn
        if len(selected_students) == 1:
            _, student_id, student_name = selected_students[0]
            confirmation_message = f"Xác nhận xóa học sinh {student_id}- {student_name}?"
        else:
            details = "\n".join([f"{stud_id}- {stud_name}" for (_, stud_id, stud_name) in selected_students])
            confirmation_message = f"Xác nhận xóa các học sinh:\n{details}"
        
        reply = QMessageBox.question(
            self, 
            "Xác nhận xóa", 
            confirmation_message,
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Xóa các dòng từ dưới lên để tránh làm lệch thứ tự
            for row, _, _ in reversed(selected_students):
                self.table.removeRow(row)
            print("Đã xóa các mục đã chọn.")
        else:
            print("Hủy xóa.")

    
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
        self.preview_data = get_right_table_data_form(get_preview_data(GET_GRADES_DATA_QUERY))
        super().__init__(
        self.preview_data,
        field= ["Chọn", "ID", "Tên", "Điểm"],
        title= "Quản lý điểm",
        main_stack =  self.main_stack,
        search_text = "Tìm kiếm học sinh",
        filter_fields = ["ID", "Tên", "Điểm"]
        )

class TuitionPage(formPage):
    def __init__(self, main_stack = None):
        self.main_stack = main_stack
        self.preview_data = get_right_table_data_form(get_preview_data(GET_TUITION_DATA_QUERY))
        super().__init__(
        self.preview_data,
        field= ["Chọn", "ID", "Tên", "Học phí","Đóng"],
        title= "Quản lý học phí",
        main_stack= self.main_stack,
        search_text = "Tìm kiếm học sinh",
        filter_fields= ["ID", "Tên", "Học phí"],
        )
