import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QGridLayout, QDialog, QFrame
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QDate, QTimer, QSize
from GUI.config import BACK_ICON_PATH, STUDENT_GRADE_PAGE_ID
from sqlQuery import GET_GRADES_DATA_BY_ID_QUERY
from GUI.util import get_right_table_data_form
from GUI.notification import FloatingNotification
from functions.functions import get_preview_data
from datetime import datetime
from functions.functions import update_student_grade


# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AltergradesPage(QWidget):
    """
    UI page for editing a student's grade.
    Displays student's name and current grade,
    allows user to update grade and save changes.
    """

    def __init__(self, parent_stack=None, student_id=None):
        """
        Initialize the AltergradesPage widget.

        Args:
            parent_stack (QStackedWidget): The parent stacked widget to enable navigation.
            student_id (int): The ID of the student whose grades are being edited.
        """
        super().__init__()
        self.parent_stack = parent_stack
        self.student_id = student_id
        self.grades_data = get_right_table_data_form(
            get_preview_data(GET_GRADES_DATA_BY_ID_QUERY.format(student_id))
        )[0] if student_id else None

        logger.info(f"Loaded grades data for student_id={student_id}")
        self.initUI()
        
    def initUI(self):
        """
        Set up the user interface for editing student grades.
        """
        self.setFont(QFont("Arial", 14))
        self.setStyleSheet("background-color: white;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Top bar with back button
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
        
        # Form layout
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)
        
        # Row 0: Student name (read-only)
        label_student_name = QLabel('Tên học sinh')
        label_student_name.setFont(QFont("Arial", 14))
        label_student_name.setStyleSheet("background: transparent; border: none;")
        self.student_name_input = QLineEdit()
        self.student_name_input.setText(self.grades_data[0] if self.grades_data else "")
        self.student_name_input.setReadOnly(True)
        self.student_name_input.setFixedHeight(30)
        form_layout.addWidget(label_student_name, 0, 0)
        form_layout.addWidget(self.student_name_input, 0, 1)

        # Row 1: Grade input
        label_grade = QLabel('Điểm')
        label_grade.setFont(QFont("Arial", 14))
        label_grade.setStyleSheet("background: transparent; border: none;")
        self.grade_line = QLineEdit()
        self.grade_line.setText(self.grades_data[1] if self.grades_data else "")
        self.grade_line.setFixedHeight(30)
        grade_layout = QHBoxLayout()
        grade_layout.addWidget(self.grade_line)
        form_layout.addWidget(label_grade, 3, 0)
        form_layout.addLayout(grade_layout, 3, 1)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()

        # Bottom layout with Save button
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.edit_button = QPushButton("Sửa điểm")
        self.edit_button.setFixedSize(150, 40)
        self.edit_button.setFont(QFont("Arial", 14))
        self.edit_button.setEnabled(True)
        self.edit_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px")
        bottom_layout.addWidget(self.edit_button)
        main_layout.addLayout(bottom_layout)
        
        # Input validation and event connections
        self.student_name_input.textChanged.connect(self.check_input)
        self.grade_line.textChanged.connect(self.check_input)
        self.edit_button.clicked.connect(self.edit_grades)

        for btn in [self.back_button, self.edit_button]:
            btn.setCursor(Qt.PointingHandCursor)
    
    def check_input(self):
        """
        Checks whether required fields are filled
        and updates the state of the edit button accordingly.
        """
        if (self.student_name_input.text().strip() and
            self.grade_line.text().strip()):
            self.edit_button.setEnabled(True)
            self.edit_button.setStyleSheet("background-color: #007BFF; color: white; border: none;")
        else:
            self.edit_button.setEnabled(False)
            self.edit_button.setStyleSheet("background-color: #A9A9A9; color: white; border: none;")
    
    def edit_grades(self):
        """
        Handles grade editing logic. Currently only prints values
        and shows a notification (replace with DB logic if needed).
        """
        name = self.student_name_input.text().strip()
        grade = self.grade_line.text().strip()
        data = [
            float(grade) if grade else None,
        
        ]
        update_student_grade(self.student_id,data)
        logger.info(f"Grade edited for student '{name}', new grade: {grade}")
        self.show_notification()
    
    def show_notification(self):
        """
        Displays a notification indicating successful grade update.
        """
        notif = FloatingNotification(
            "Sửa điểm thành công!",
            parent=self.parent_stack,
            bg_color="#28a745",
            icon_path=r"C:\Project_Python\applications\grades-Manager\app\assets\ok.png",
        )
        notif.show_bottom_center()
    
    def go_back(self):
        """
        Navigates back to the grade list page.
        """
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(STUDENT_GRADE_PAGE_ID)
            logger.info("Navigated back to student grade list page.")
        else:
            logger.warning("Parent stack not set. Cannot navigate back.")
