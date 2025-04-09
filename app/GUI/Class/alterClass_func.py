import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDialog, QListWidgetItem, QGridLayout
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
from GUI.config import BACK_ICON_PATH, CLASS_PAGE_ID
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_CLASS_DATA_BY_ID_QUERY
from GUI.notification import FloatingNotification
from GUI.Student.studentSelector import StudentSelectorDialog
from GUI.Teacher.teacherSelector import TeacherSelectorDialog
from functions.functions import update_class_info
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlterClassPage(QWidget):
    """
    This class represents a UI page that allows the user to edit an existing class.
    Users can modify the class name, assign a teacher, and select students.
    """
    
    def __init__(self, parent_stack=None, class_id=None):
        """
        Initializes the AlterClassPage widget.

        Args:
            parent_stack (QStackedWidget): The stacked widget containing this page.
            class_id (int): The ID of the class to be edited.
        """
        super().__init__()
        self.parent_stack = parent_stack
        self.class_id = class_id

        # Fetch class data from database if class_id is provided
        self.class_data = get_right_table_data_form(
            get_preview_data(GET_CLASS_DATA_BY_ID_QUERY.format(class_id))
        )[0] if class_id else None

        

        # Extract teacher and student IDs
        self.teacher_id = self.class_data[3] if self.class_data else None
        self.students_id = self.class_data[4].split(",") if self.class_data else []
        self.selected_students = self.students_id.copy()
        self.selected_teacher = self.teacher_id

        logger.info(f"Loaded class data for class_id={class_id}")
        self.initUI()

    def initUI(self):
        """
        Sets up the UI components and layout for the class edit form.
        """
        self.setFont(QFont("Arial", 14))
        self.setStyleSheet("background-color: white;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Top layout: back button
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
        
        # Form layout for class data
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)
        
        # Row 0: Class name
        label_class_name = QLabel('Tên lớp')
        label_class_name.setStyleSheet("background: transparent; border: none;")
        self.class_name_input = QLineEdit()
        self.class_name_input.setText(self.class_data[0] if self.class_data else "")
        self.class_name_input.setFixedHeight(30)
        form_layout.addWidget(label_class_name, 0, 0)
        form_layout.addWidget(self.class_name_input, 0, 1)
        
        # Row 2: Student selector
        label_students = QLabel('Học sinh')
        label_students.setStyleSheet("background: transparent; border: none;")
        self.students_line = QLineEdit()
        self.students_line.setText(self.class_data[1] if self.class_data else "")
        self.students_line.setReadOnly(True)
        self.students_line.setFixedHeight(30)
        self.btn_select_students = QPushButton("Xem|Sửa")
        self.btn_select_students.setFixedSize(150, 35)
        self.btn_select_students.clicked.connect(self.open_student_selector)
        students_layout = QHBoxLayout()
        students_layout.addWidget(self.students_line)
        students_layout.addWidget(self.btn_select_students)
        form_layout.addWidget(label_students, 2, 0)
        form_layout.addLayout(students_layout, 2, 1)
        
        # Row 3: Teacher selector
        label_teacher = QLabel('Giáo viên')
        label_teacher.setStyleSheet("background: transparent; border: none;")
        self.teacher_line = QLineEdit()
        self.teacher_line.setText(f'ID giáo viên: {self.teacher_id}')
        self.teacher_line.setReadOnly(True)
        self.teacher_line.setFixedHeight(30)
        self.btn_select_teacher = QPushButton("Xem|Sửa")
        self.btn_select_teacher.setFixedSize(150, 35)
        self.btn_select_teacher.clicked.connect(self.open_teacher_selector)
        teacher_layout = QHBoxLayout()
        teacher_layout.addWidget(self.teacher_line)
        teacher_layout.addWidget(self.btn_select_teacher)
        form_layout.addWidget(label_teacher, 3, 0)
        form_layout.addLayout(teacher_layout, 3, 1)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        
        # Save button (disabled initially)
        self.edit_button = QPushButton("Sửa lớp học")
        self.edit_button.setFixedSize(150, 40)
        self.edit_button.setFont(QFont("Arial", 14))
        self.edit_button.setEnabled(False)
        self.edit_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px;")
        self.edit_button.clicked.connect(self.edit_class)
        main_layout.addWidget(self.edit_button, alignment=Qt.AlignRight)
        
        # Enable save button only if class name and teacher are selected
        self.class_name_input.textChanged.connect(self.check_input)

        for btn in [self.back_button, self.edit_button]:
            btn.setCursor(Qt.PointingHandCursor)

    def check_input(self):
        """
        Enables or disables the edit button depending on input validity.
        """
        if self.class_name_input.text().strip() and self.selected_teacher:
            self.edit_button.setEnabled(True)
            self.edit_button.setStyleSheet("background-color: #007BFF; color: white; border-radius: 8px;")
        else:
            self.edit_button.setEnabled(False)
            self.edit_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px;")

    def open_student_selector(self):
        """
        Opens the student selection dialog and updates selected student list.
        """
        dialog = StudentSelectorDialog(self, students_id=self.students_id)
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.get_selection()
            if selected:
                _ids = [row[0] for row in selected]
                self.selected_students = _ids
                self.students_line.setText(str(len(_ids)))
                logger.info(f"Selected students: {self.selected_students}")
            else:
                self.students_line.setText(self.class_data[1] if self.class_data else "")

    def open_teacher_selector(self):
        """
        Opens the teacher selection dialog and updates selected teacher.
        """
        dialog = TeacherSelectorDialog(self, teacher_id=self.teacher_id)
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.get_selection()
            if selected:
                self.selected_teacher = selected[0]
                self.teacher_line.setText(f"ID giáo viên: {self.selected_teacher}")
                logger.info(f"Selected teacher: {self.selected_teacher}")
            else:
                self.teacher_line.setText("Chưa chọn giáo viên")
            self.check_input()

    def edit_class(self):
        """
        Handles the logic for editing the class and shows a success notification.
        """
        class_name = self.class_name_input.text().strip()
        teacher = self.selected_teacher # id giáo viên
        len_students = len(self.selected_students)

        data = [
            class_name,
            len_students,
            teacher

        ]
        update_class_info(self.class_id,data,student_ids = self.selected_students)
        

        logger.info(f"Editing class: {class_name}, Teacher ID: {teacher}, Student nums: {len_students}")
        
        # Placeholder for actual database update
        self.show_notification()

    def show_notification(self):
        """
        Displays a success notification after class is edited.
        """
        notif = FloatingNotification(
            "Sửa lớp học thành công!",
            parent=self.parent_stack,
            bg_color="#28a745",
            icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
        )
        notif.show_bottom_center()

    def go_back(self):
        """
        Navigates back to the class list page.
        """
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(CLASS_PAGE_ID)
            logger.info("Navigated back to class list page.")
        else:
            logger.warning("Parent stack not set. Cannot go back.")
