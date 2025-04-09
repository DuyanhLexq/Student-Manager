# -*- coding: utf-8 -*-
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize,Qt
from GUI.config import BACK_ICON_PATH, TEACHER_SALARY_PAGE_ID
from GUI.notification import FloatingNotification
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import  CHECK_TEACHER_NAME_QUERY
from GUI.Teacher.alterSalary_func import AlterSalaryPage
from GUI.Teacher.addTeacher_func import AddTeacherPage

# Configure module-level logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AddSalaryPage(QWidget):
    """
    A page for adding teacher salary information.

    Attributes:
        parent_stack: The QStackedWidget used for navigation between pages.
    """
    def __init__(self, parent_stack=None):
        """
        Initializes the AddSalaryPage.

        Args:
            parent_stack: The parent QStackedWidget for navigation.
        """
        super().__init__()
        self.parent_stack = parent_stack
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface for adding teacher salary information.
        """
        # Set common font for the form
        self.setFont(QFont("Arial", 14))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Top layout: Back button
        top_layout = QHBoxLayout()
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(BACK_ICON_PATH))
        self.back_button.setIconSize(QSize(32, 32))
        self.back_button.setFlat(True)
        self.back_button.setStyleSheet("border: none; background: transparent;")
        self.back_button.clicked.connect(self.go_back)
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        layout.addLayout(top_layout)
        
        # Row 1: Teacher Name (required)
        row1 = QHBoxLayout()
        label_name = QLabel('Tên Giáo viên <span style="color:red; font-size:16px;">*</span>')
        label_name.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên giáo viên")
        self.name_input.setFixedHeight(30)
        row1.addWidget(label_name)
        row1.addWidget(self.name_input)
        layout.addLayout(row1)
        
        # Row 2: Salary (required)
        row2 = QHBoxLayout()
        label_salary = QLabel('Lương <span style="color:red; font-size:16px;">*</span>')
        label_salary.setFont(QFont("Arial", 14))
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("Nhập lương")
        self.salary_input.setFixedHeight(30)
        row2.addWidget(label_salary)
        row2.addWidget(self.salary_input)
        layout.addLayout(row2)
        
        # Row 3: Bonus (optional)
        row3 = QHBoxLayout()
        label_bonus = QLabel("Lương thưởng")
        label_bonus.setFont(QFont("Arial", 14))
        self.bonus_input = QLineEdit()
        self.bonus_input.setPlaceholderText("Nhập lương thưởng")
        self.bonus_input.setFixedHeight(30)
        row3.addWidget(label_bonus)
        row3.addWidget(self.bonus_input)
        layout.addLayout(row3)
        layout.addStretch()
        
        # Bottom layout: "Thêm" button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.add_button = QPushButton("Thêm")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        self.add_button.setEnabled(False)
        self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px")
        self.add_button.clicked.connect(self.add_salary)
        bottom_layout.addWidget(self.add_button)
        layout.addLayout(bottom_layout)
        
        # Connect signals for input validation
        self.name_input.textChanged.connect(self.check_input)
        self.salary_input.textChanged.connect(self.check_input)
        for btn in [self.back_button, self.add_button]:
            btn.setCursor(Qt.PointingHandCursor)
        
        logger.info("AddSalaryPage UI initialized.")

    def check_input(self):
        """
        Validates that the required fields (Tên Giáo viên and Lương) are not empty.
        Enables or disables the submit button accordingly.
        """
        if self.name_input.text().strip() and self.salary_input.text().strip():
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px")
            logger.debug("Input validation passed; submit button enabled.")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px")
            logger.debug("Input validation failed; submit button disabled.")

    def add_salary(self):
        """
        Processes the entered salary information.
        Logs the information and displays a floating notification upon success.
        """
        name = self.name_input.text().strip()
        salary = self.salary_input.text().strip()
        bonus = self.bonus_input.text().strip()
        teachers_exists = get_right_table_data_form(get_preview_data(CHECK_TEACHER_NAME_QUERY.format(name)))
        if teachers_exists:
            # Nếu học sinh đã có trong hệ thống, hỏi người dùng có muốn sửa điểm không.
            reply = QMessageBox.question(
                self,
                'Sửa lương?',
                f"Có vẻ như lương của giáo viên {name} đã có trong hệ thống. Bạn có muốn sửa không?. Nếu đây là một giáo viên mới, hãy thêm  trước khi nhập lương nhé !😊",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                # Chuyển sang trang sửa lương.
                add_page = AlterSalaryPage(parent_stack=self.parent_stack,teacher_id=teachers_exists[0][0])
                self.parent_stack.addWidget(add_page)
                self.parent_stack.setCurrentWidget(add_page)
            elif reply == QMessageBox.No:
                self.show_notification()
            

                

        else:
            # Nếu học sinh chưa có trong hệ thống, hỏi người dùng có muốn thêm học sinh mới không.
            reply = QMessageBox.question(
                self,
                'Thêm giáo viên?',
                f"Giáo viên {name} chưa có trong hệ thống. Bạn có muốn thêm  mới không? 😎",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                add_page = AddTeacherPage(parent_stack=self.parent_stack)
                self.parent_stack.addWidget(add_page)
                self.parent_stack.setCurrentWidget(add_page)
            elif reply == QMessageBox.No:
                # Hiển thị thông báo và quay lại.
                self.show_notification()

        logger.info("Thêm lương: %s, %s, %s", name, salary, bonus)
        # Here you would typically insert the salary data into the database.

    def show_notification(self):
        """
        Displays a floating notification indicating that the salary has been added successfully.
        """
        try:
            notif = FloatingNotification(
                "Thêm lương thành công!",
                parent=self.parent_stack,
                bg_color="#28a745",  # Màu xanh lá
                icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
            )
            notif.show_bottom_center()
            logger.info("Floating notification displayed for salary addition.")
        except Exception as e:
            logger.error("Error displaying floating notification: %s", e)

    def go_back(self):
        """
        Navigates back to the teacher salary management page using the parent_stack.
        """
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(TEACHER_SALARY_PAGE_ID)
            logger.info("Navigated back to teacher salary management page.")
        else:
            logger.error("Parent stack not provided; cannot navigate back.")
