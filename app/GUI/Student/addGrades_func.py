import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QGridLayout
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from GUI.config import BACK_ICON_PATH, STUDENT_GRADE_PAGE_ID
from GUI.notification import FloatingNotification

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AddGradePage(QWidget):
    """
    UI page for adding a grade to a student.
    Allows user to input student name and grade, then add to the system.
    """
    def __init__(self, parent_stack=None):
        """
        Initialize the AddGradePage widget.

        Args:
            parent_stack (QStackedWidget): The parent stack to allow navigation.
        """
        super().__init__()
        self.parent_stack = parent_stack
        self.selected_grade = None
        self.selected_students = []
        self.initUI()
    
    def initUI(self):
        """
        Initialize all UI components.
        """
        self.setFont(QFont("Arial", 14))
        self.setStyleSheet("background-color: white;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Top bar: Back button
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
        
        # Row 0: Student Name
        label_student_name = QLabel('Tên học sinh <span style="color:red; font-size:16px;">*</span>')
        label_student_name.setFont(QFont("Arial", 14))
        label_student_name.setStyleSheet("background: transparent; border: none;")
        self.student_name_input = QLineEdit()
        self.student_name_input.setPlaceholderText("Nhập tên học sinh")
        self.student_name_input.setFixedHeight(30)
        form_layout.addWidget(label_student_name, 0, 0)
        form_layout.addWidget(self.student_name_input, 0, 1)
        
        # Row 1: Grade input
        label_grade = QLabel('Điểm <span style="color:red; font-size:16px;">*</span>')
        label_grade.setFont(QFont("Arial", 14))
        label_grade.setStyleSheet("background: transparent; border: none;")
        self.grade_line = QLineEdit()
        self.grade_line.setPlaceholderText("Nhập điểm")
        self.grade_line.setFixedHeight(30)
        form_layout.addWidget(label_grade, 1, 0)
        form_layout.addWidget(self.grade_line, 1, 1)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        
        # Add button (bottom-right)
        self.add_button = QPushButton("Thêm điểm")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        self.add_button.setEnabled(False)
        self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px;")
        self.add_button.clicked.connect(self.add_grade)
        main_layout.addWidget(self.add_button, alignment=Qt.AlignRight)
        
        # Input change connections for validation
        self.student_name_input.textChanged.connect(self.check_input)
        self.grade_line.textChanged.connect(self.check_input)
    
    def check_input(self):
        """
        Enable/disable the Add button depending on whether
        required fields are filled in.
        """
        if self.student_name_input.text().strip() and self.grade_line.text().strip():
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white; border: none; border-radius: 8px;")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border: none; border-radius: 8px;")
    
    def add_grade(self):
        """
        Handles adding the grade logic.
        Prints info to console and shows a success notification.
        """
        student_name = self.student_name_input.text().strip()
        grade = self.grade_line.text().strip()

        if not student_name or not grade:
            logger.warning("Missing student name or grade.")
            return

        # 👉 TODO: Replace this with actual DB insert logic
        logger.info(f"Adding grade: Student='{student_name}', Grade={grade}")
        self.show_notification()
    
    def show_notification(self):
        """
        Shows a floating notification to confirm grade was added.
        """
        notif = FloatingNotification(
            "Thêm điểm thành công!",
            parent=self.parent_stack,
            bg_color="#28a745",
            icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
        )
        notif.show_bottom_center()
    
    def go_back(self):
        """
        Navigates back to the student grade page.
        """
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(STUDENT_GRADE_PAGE_ID)
            logger.info("Navigated back to grade list page.")
        else:
            logger.warning("Parent stack not provided.")
