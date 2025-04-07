# -*- coding: utf-8 -*-
import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QDialog, QDialogButtonBox, QListWidgetItem, QFrame, QGridLayout, QComboBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QSize
from GUI.config import BACK_ICON_PATH, STUDENT_FEE_PAGE_ID
from sqlQuery import GET_TUITION_DATA_BY_ID_QUERY
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from GUI.notification import FloatingNotification

# Configure module-level logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AlterFeePage(QWidget):
    """
    A page for editing the tuition fee information of a student.

    Attributes:
        parent_stack: The QStackedWidget used for navigation between pages.
        fee_data: A list containing tuition fee data retrieved from the database.
                  Expected format: [Tên học sinh, Học phí, Đóng]
    """
    def __init__(self, parent_stack=None, student_id=None):
        """
        Initializes the AlterFeePage.

        Args:
            parent_stack: The parent QStackedWidget for navigation.
            student_id (str): The student's ID to load tuition fee data.
        """
        super().__init__()
        self.parent_stack = parent_stack
        try:
            raw_data = get_preview_data(GET_TUITION_DATA_BY_ID_QUERY.format(student_id))
            fee_list = get_right_table_data_form(raw_data)
            self.fee_data = fee_list[0] if fee_list else None
            logger.info("Tuition fee data loaded successfully for student ID: %s", student_id)
        except Exception as e:
            logger.error("Error retrieving tuition fee data for student ID %s: %s", student_id, e)
            self.fee_data = None
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface for editing student tuition fee information.
        """
        self.setFont(QFont("Arial", 14))
        self.setStyleSheet("background-color: white;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
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
        main_layout.addLayout(top_layout)
        
        # Form layout using a grid for proper alignment
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)
        
        # Student Name (read-only)
        label_student_name = QLabel("Tên học sinh")
        label_student_name.setFont(QFont("Arial", 14))
        label_student_name.setStyleSheet("background: transparent; border: none;")
        self.student_name_input = QLineEdit()
        self.student_name_input.setText(self.fee_data[0] if self.fee_data else "")
        self.student_name_input.setReadOnly(True)
        self.student_name_input.setFixedHeight(30)
        form_layout.addWidget(label_student_name, 0, 0)
        form_layout.addWidget(self.student_name_input, 0, 1)
        
        # Tuition Fee
        label_fee = QLabel("Học phí")
        label_fee.setFont(QFont("Arial", 14))
        label_fee.setStyleSheet("background: transparent; border: none;")
        self.fee_line = QLineEdit()
        self.fee_line.setText(self.fee_data[1] if self.fee_data else "")
        self.fee_line.setFixedHeight(30)
        fee_layout = QHBoxLayout()
        fee_layout.addWidget(self.fee_line)
        form_layout.addWidget(label_fee, 3, 0)
        form_layout.addLayout(fee_layout, 3, 1)
        
        # Payment Status (ComboBox)
        label_paid = QLabel("Đóng")
        label_paid.setFont(QFont("Arial", 14))
        label_paid.setStyleSheet("background: transparent; border: none;")
        self.paid_combo = QComboBox()
        self.paid_combo.addItems(["Đã đóng", "Chưa đóng"])
        self.paid_combo.setCurrentText(self.fee_data[2] if self.fee_data else "Chưa đóng")
        self.paid_combo.setFixedHeight(30)
        self.paid_combo.setStyleSheet("QComboBox { background-color: white; }")
        paid_layout = QHBoxLayout()
        paid_layout.addWidget(self.paid_combo)
        form_layout.addWidget(label_paid, 4, 0)
        form_layout.addLayout(paid_layout, 4, 1)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        
        # Bottom layout: Edit Fee button
        self.edit_button = QPushButton("Sửa học phí")
        self.edit_button.setFixedSize(150, 40)
        self.edit_button.setFont(QFont("Arial", 14))
        self.edit_button.setEnabled(False)
        self.edit_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px;")
        self.edit_button.clicked.connect(self.edit_fee)
        main_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)
        
        # Connect signals for input validation
        self.student_name_input.textChanged.connect(self.check_input)
        self.fee_line.textChanged.connect(self.check_input)
        self.paid_combo.currentTextChanged.connect(self.check_input)
        
        logger.info("AlterFeePage UI initialized.")

    def check_input(self):
        """
        Validates that the required fields (Tên học sinh, Học phí, Đóng) are not empty.
        Enables or disables the edit button accordingly.
        """
        if self.student_name_input.text().strip() and self.fee_line.text().strip() and self.paid_combo.currentText():
            self.edit_button.setEnabled(True)
            self.edit_button.setStyleSheet("background-color: #007BFF; color: white; border: none; border-radius: 8px;")
            logger.debug("Input validation passed; edit button enabled.")
        else:
            self.edit_button.setEnabled(False)
            self.edit_button.setStyleSheet("background-color: #A9A9A9; color: white; border: none; border-radius: 8px;")
            logger.debug("Input validation failed; edit button disabled.")

    def edit_fee(self):
        """
        Processes the tuition fee information entered by the user.
        Logs the updated information and displays a floating notification upon success.
        """
        student_name = self.student_name_input.text().strip()
        fee = self.fee_line.text().strip()
        paid = self.paid_combo.currentText()
        
        # Check if required fields are provided (this is a safeguard)
        if not student_name or not fee or not paid:
            logger.warning("Insufficient information to update tuition fee.")
            print("Vui lòng nhập đầy đủ thông tin.")
            return
        
        logger.info("Sửa Học phí: %s, Học phí: %s, Đã đóng: %s", student_name, fee, paid)
        # Here, update the fee data in the database as needed.
        self.show_notification()

    def show_notification(self):
        """
        Displays a floating notification indicating that the tuition fee update was successful.
        """
        try:
            notif = FloatingNotification(
                "Sửa học phí thành công!",
                parent=self.parent_stack,
                bg_color="#28a745",  # Màu xanh lá
                icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
            )
            notif.show_bottom_center()
            logger.info("Floating notification displayed for tuition fee update.")
        except Exception as e:
            logger.error("Error displaying floating notification: %s", e)

    def go_back(self):
        """
        Navigates back to the student fee management page using the parent_stack.
        """
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(STUDENT_FEE_PAGE_ID)
            logger.info("Navigated back to STUDENT_FEE_PAGE_ID.")
        else:
            logger.error("Parent stack not provided; cannot navigate back.")
