# -*- coding: utf-8 -*-
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDateEdit, QDialog, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from GUI.config import BACK_ICON_PATH, TEACHER_SALARY_PAGE_ID
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_SALARY_DATA_BY_ID_QUERY
from GUI.notification import FloatingNotification

# Configure module-level logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlterSalaryPage(QWidget):
    """
    A page for editing teacher salary information.

    Attributes:
        parent_stack: The QStackedWidget used for navigation between pages.
        salary_data: A list containing the teacher's salary data, retrieved from the database.
                     Expected format: [Tên Giáo viên, Lương, Lương thưởng]
    """

    def __init__(self, parent_stack=None, teacher_id=None):
        """
        Initializes the AlterSalaryPage.

        Args:
            parent_stack: The parent QStackedWidget for navigation.
            teacher_id (str): The teacher's ID to load the salary data for editing.
        """
        super().__init__()
        self.parent_stack = parent_stack
        try:
            raw_data = get_preview_data(GET_SALARY_DATA_BY_ID_QUERY.format(teacher_id))
            salary_list = get_right_table_data_form(raw_data)
            self.salary_data = salary_list[0] if salary_list else None
            logger.info("Salary data loaded successfully for teacher ID: %s", teacher_id)
        except Exception as e:
            logger.error("Error retrieving salary data for teacher ID %s: %s", teacher_id, e)
            self.salary_data = None
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface for editing teacher salary information.
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

        # Row 1: Teacher Name (readonly)
        row1 = QHBoxLayout()
        label_name = QLabel("Tên Giáo viên")
        label_name.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        self.name_input.setText(self.salary_data[0] if self.salary_data else "")
        self.name_input.setReadOnly(True)
        self.name_input.setFixedHeight(30)
        row1.addWidget(label_name)
        row1.addWidget(self.name_input)
        layout.addLayout(row1)

        # Row 2: Salary (required)
        row2 = QHBoxLayout()
        label_salary = QLabel("Lương")
        label_salary.setFont(QFont("Arial", 14))
        self.salary_input = QLineEdit()
        self.salary_input.setText(self.salary_data[1] if self.salary_data else "")
        self.salary_input.setFixedHeight(30)
        row2.addWidget(label_salary)
        row2.addWidget(self.salary_input)
        layout.addLayout(row2)

        # Row 3: Bonus (optional)
        row3 = QHBoxLayout()
        label_bonus = QLabel("Lương thưởng")
        label_bonus.setFont(QFont("Arial", 14))
        self.bonus_input = QLineEdit()
        self.bonus_input.setText(self.salary_data[2] if self.salary_data else "")
        self.bonus_input.setFixedHeight(30)
        row3.addWidget(label_bonus)
        row3.addWidget(self.bonus_input)
        layout.addLayout(row3)
        layout.addStretch()

        # Bottom layout: "Sửa" button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.add_button = QPushButton("Sửa")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        self.add_button.setEnabled(True)
        self.add_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px")
        self.add_button.clicked.connect(self.add_salary)
        bottom_layout.addWidget(self.add_button)
        layout.addLayout(bottom_layout)

        # Connect signals for input validation
        self.name_input.textChanged.connect(self.check_input)
        self.salary_input.textChanged.connect(self.check_input)

        logger.info("AlterSalaryPage UI initialized.")

    def check_input(self):
        """
        Validates that the required fields (Tên Giáo viên and Lương) are not empty.
        Enables or disables the submit button accordingly.
        """
        if self.name_input.text().strip() and self.salary_input.text().strip():
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px")
            logger.debug("Input validation passed; button enabled.")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px")
            logger.debug("Input validation failed; button disabled.")

    def add_salary(self):
        """
        Processes the salary information entered by the user.
        Logs the information and displays a floating notification upon success.
        """
        name = self.name_input.text().strip()
        salary = self.salary_input.text().strip()
        bonus = self.bonus_input.text().strip()
        logger.info("Sửa lương: %s, %s, %s", name, salary, bonus)
        # Here you can add the logic to update the salary in the database.
        self.show_notification()

    def show_notification(self):
        """
        Displays a floating notification indicating that the salary update was successful.
        """
        try:
            notif = FloatingNotification(
                "Sửa lương thành công!",
                parent=self.parent_stack,
                bg_color="#28a745",  # Màu xanh lá
                icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
            )
            notif.show_bottom_center()
            logger.info("Floating notification displayed.")
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
            logger.error("Parent stack not available; cannot navigate back.")

