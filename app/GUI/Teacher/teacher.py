# File: teacher.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.Teacher.addTeacher_func import AddTeacherPage
from GUI.util import formPage

class TeacherPage(formPage):
    def __init__(self, main_stack=None):
        self.main_stack = main_stack
        super().__init__(
            data=[
                ["GV001", "Nguyễn Văn A", "01/01/1980", "2010"],
                ["GV002", "Trần Thị B", "05/03/1985", "2012"],
                ["GV003", "Lê Văn C", "12/07/1978", "2008"]
            ],
            field=["Chọn", "ID", "Tên giáo viên", "Ngày sinh", "Năm vào làm việc"],
            title="Quản lý giáo viên",
            main_stack=self.main_stack,
            search_text="Tìm kiếm giáo viên",
            filter_fields=["Tên giáo viên", "Năm vào làm việc", "ID"]
        )
  
    def go_to_add_page(self):
        if self.main_stack:
            # Ví dụ: Khởi tạo trang thêm mới giáo viên
            add_page = AddTeacherPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
        else:
            print("Main stack chưa được cung cấp!")

class SalaryPage(formPage):
    def __init__(self,main_stack = None):
        self.main_stack  = main_stack
        super().__init__(
            [
                ["GV001","Nguyễn Văn A","100$","2$"],
                ["GV002", "Trần Thị B", "120$", "1$"],
                ["GV003", "Lê Văn C", "110$", "3$"]

            ],
            ["Chọn", "ID", "Tên giáo viên", "Lương", "Lương thưởng"],
            title= "Quản lý lương giáo viên",
            main_stack= self.main_stack,
            search_text = "Tìm kiếm giáo viên",
            filter_fields = ["ID","Tên giáo viên","Lương","Lương thưởng"]
        )
    


