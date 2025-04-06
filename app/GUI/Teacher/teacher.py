# File: teacher.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from GUI.Teacher.addTeacher_func import AddTeacherPage
from GUI.util import formPage,get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_PREVIEW_SALARY_DATA_QUERY,GET_PREVIEW_TEACHER_DATA_QUERY
from typing import List
class TeacherPage(formPage):
    def __init__(self, main_stack=None):
        self.main_stack = main_stack
        self.preview_data = get_right_table_data_form(get_preview_data(GET_PREVIEW_TEACHER_DATA_QUERY))
        
        super().__init__(
            data= self.preview_data,
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
        self.preview_data = get_right_table_data_form(get_preview_data(GET_PREVIEW_SALARY_DATA_QUERY))
        super().__init__(
            self.preview_data,
            ["Chọn", "ID", "Tên giáo viên", "Lương", "Lương thưởng"],
            title= "Quản lý lương giáo viên",
            main_stack= self.main_stack,
            search_text = "Tìm kiếm giáo viên",
            filter_fields = ["ID","Tên giáo viên","Lương","Lương thưởng"]
        )