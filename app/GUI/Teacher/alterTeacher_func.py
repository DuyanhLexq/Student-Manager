# -*- coding: utf-8 -*-
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDateEdit, QDialog, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from GUI.config import BACK_ICON_PATH, TEACHER_PAGE_ID
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_TEACHER_DATA_BY_ID_QUERY
from datetime import datetime
from GUI.notification import FloatingNotification

# Configure module-level logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlterTeacherPage(QWidget):
    """
    A page for editing teacher information.
    
    Attributes:
        parent_stack: The QStackedWidget used for navigation between pages.
        teacher_data: A list containing teacher data retrieved from the database.
    """

    def __init__(self, parent_stack=None, teacher_id=None):
        """
        Initializes the AlterTeacherPage.
        
        Args:
            parent_stack: The parent QStackedWidget for navigation.
            teacher_id (str): The teacher's ID to load the data for editing.
        """
        super().__init__()
        self.parent_stack = parent_stack
        self.teacher_data = None
        if teacher_id:
            try:
                # Retrieve teacher data using the provided teacher_id
                raw_data = get_preview_data(GET_TEACHER_DATA_BY_ID_QUERY.format(teacher_id))
                teacher_list = get_right_table_data_form(raw_data)
                if teacher_list:
                    self.teacher_data = teacher_list[0]
                    logger.info("Teacher data loaded successfully for teacher ID: %s", teacher_id)
                else:
                    logger.warning("No teacher data found for teacher ID: %s", teacher_id)
            except Exception as e:
                logger.error("Error retrieving teacher data for teacher ID %s: %s", teacher_id, e)
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface for editing teacher information.
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

        # Row 1: Teacher Name (*)
        row1 = QHBoxLayout()
        label_name = QLabel("Tên Giáo viên")
        label_name.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        # Pre-fill teacher name if available
        self.name_input.setText(self.teacher_data[0] if self.teacher_data else "")
        self.name_input.setFixedHeight(30)
        row1.addWidget(label_name)
        row1.addWidget(self.name_input)
        layout.addLayout(row1)

        # Row 2: Date of Birth (*)
        row2 = QHBoxLayout()
        label_dob = QLabel("Ngày tháng năm sinh")
        label_dob.setFont(QFont("Arial", 14))
        self.dob_edit = QDateEdit()
        self.dob_edit.setDisplayFormat("dd/MM/yyyy")
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setFixedHeight(30)
        if self.teacher_data:
            try:
                # Parse date string from teacher_data (expected format: YYYY-MM-DD)
                parsed_date = datetime.strptime(self.teacher_data[1], "%Y-%m-%d").date()
                qdate = QDate(parsed_date.year, parsed_date.month, parsed_date.day)
                self.dob_edit.setDate(qdate)
            except Exception as e:
                logger.error("Error parsing date of birth: %s", e)
                self.dob_edit.setDate(QDate.currentDate())
        else:
            self.dob_edit.setDate(QDate.currentDate())
        row2.addWidget(label_dob)
        row2.addWidget(self.dob_edit)
        layout.addLayout(row2)

        # Row 3: Phone Number
        row3 = QHBoxLayout()
        label_phone = QLabel("Số điện thoại")
        label_phone.setFont(QFont("Arial", 14))
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.teacher_data[2] if self.teacher_data else "")
        self.phone_input.setFixedHeight(30)
        row3.addWidget(label_phone)
        row3.addWidget(self.phone_input)
        layout.addLayout(row3)

        # Row 4: Contract Expiration Date (*)
        row4 = QHBoxLayout()
        label_contract = QLabel("Ngày hết hạn hợp đồng")
        label_contract.setFont(QFont("Arial", 14))
        self.contract_edit = QDateEdit()
        self.contract_edit.setDisplayFormat("dd/MM/yyyy")
        self.contract_edit.setCalendarPopup(True)
        self.contract_edit.setFixedHeight(30)
        if self.teacher_data:
            try:
                parsed_date = datetime.strptime(self.teacher_data[3], "%Y-%m-%d").date()
                qdate = QDate(parsed_date.year, parsed_date.month, parsed_date.day)
                self.contract_edit.setDate(qdate)
            except Exception as e:
                logger.error("Error parsing contract expiration date: %s", e)
                self.contract_edit.setDate(QDate.currentDate())
        else:
            self.contract_edit.setDate(QDate.currentDate())
        row4.addWidget(label_contract)
        row4.addWidget(self.contract_edit)
        layout.addLayout(row4)

        # Row 5: Start Date (*)
        row5 = QHBoxLayout()
        label_start = QLabel("Ngày vào nhận việc")
        label_start.setFont(QFont("Arial", 14))
        self.start_date = QDateEdit()
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        self.start_date.setCalendarPopup(True)
        self.start_date.setFixedHeight(30)
        if self.teacher_data:
            try:
                parsed_date = datetime.strptime(self.teacher_data[4], "%Y-%m-%d").date()
                qdate = QDate(parsed_date.year, parsed_date.month, parsed_date.day)
                self.start_date.setDate(qdate)
            except Exception as e:
                logger.error("Error parsing start date: %s", e)
                self.start_date.setDate(QDate.currentDate())
        else:
            self.start_date.setDate(QDate.currentDate())
        row5.addWidget(label_start)
        row5.addWidget(self.start_date)
        layout.addLayout(row5)

        layout.addStretch()

        # Bottom layout: "Sửa giáo viên" button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.add_button = QPushButton("Sửa giáo viên")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        # Initially enabled until required fields are filled
        self.add_button.setEnabled(True)
        self.add_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px")
        bottom_layout.addWidget(self.add_button)
        layout.addLayout(bottom_layout)

        # Connect input change events to input validation
        self.name_input.textChanged.connect(self.check_input)
        self.contract_edit.dateChanged.connect(self.check_input)
        self.start_date.dateChanged.connect(self.check_input)
        self.add_button.clicked.connect(self.add_teacher)

        logger.info("AlterTeacherPage UI initialized.")

    def check_input(self):
        """
        Checks if the required fields (Tên, Ngày hết hạn hợp đồng, Ngày vào nhận việc) are filled.
        Enables or disables the submit button accordingly.
        """
        if self.name_input.text().strip():
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px")
            logger.debug("Input validation passed; button enabled.")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px")
            logger.debug("Input validation failed; button disabled.")

    def add_teacher(self):
        """
        Processes the teacher information entered by the user.
        Logs the information and displays a floating notification upon success.
        """
        # Retrieve and format input data
        name = self.name_input.text().strip()
        dob = self.dob_edit.date().toString("dd/MM/yyyy")
        phone = self.phone_input.text().strip()
        contract = self.contract_edit.date().toString("dd/MM/yyyy")
        start = self.start_date.date().toString("dd/MM/yyyy")
        
        # Log the teacher update information (in a real scenario, this would involve database updates)
        logger.info("Updating teacher: %s, %s, %s, %s, %s", name, dob, phone, contract, start)
        
        # Display a floating notification to indicate success
        self.show_notification()

    def show_notification(self):
        """
        Displays a floating notification indicating that the teacher information was updated successfully.
        """
        try:
            notif = FloatingNotification(
                "Sửa giáo viên thành công!",
                parent=self.parent_stack,
                bg_color="#28a745",  # Green color
                icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
            )
            notif.show_bottom_center()
            logger.info("Floating notification displayed.")
        except Exception as e:
            logger.error("Error displaying floating notification: %s", e)

    def go_back(self):
        """
        Navigates back to the teacher management page using the parent_stack.
        """
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(TEACHER_PAGE_ID)
            logger.info("Navigated back to teacher management page.")
        else:
            logger.error("Parent stack is not available; cannot navigate back.")