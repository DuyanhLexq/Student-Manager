from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QDialog, QDialogButtonBox, QListWidgetItem, QFrame,QGridLayout
)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt, QTimer,QSize
from GUI.config import BACK_ICON_PATH,CLASS_PAGE_ID
from GUI.Student.studentSelector import StudentSelectorDialog
from GUI.Teacher.teacherSelector import TeacherSelectorDialog

class AddClassPage(QWidget):
    def __init__(self, parent_stack=None):
        super().__init__()
        self.parent_stack = parent_stack
        self.selected_teacher = None
        self.selected_students = []
        self.initUI()
    
    def initUI(self):
        self.setFont(QFont("Arial", 14))
        self.setStyleSheet("background-color: white;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Top layout: Nút quay lại
        top_layout = QHBoxLayout()
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon(BACK_ICON_PATH))
        self.back_button.setIconSize(QSize(32,32))
        self.back_button.setFlat(True)
        self.back_button.setStyleSheet("border: none; background: transparent;")
        self.back_button.clicked.connect(self.go_back)
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)
        
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)
        
        # Hàng 0: Tên lớp
        label_class_name = QLabel('Tên lớp <span style="color:red; font-size:16px;">*</span>')
        label_class_name.setFont(QFont("Arial", 14))
        label_class_name.setStyleSheet("background: transparent; border: none;")
        self.class_name_input = QLineEdit()
        self.class_name_input.setPlaceholderText("Nhập tên lớp")
        self.class_name_input.setFixedHeight(30)
        form_layout.addWidget(label_class_name, 0, 0, 1, 2)
        form_layout.addWidget(self.class_name_input, 1, 0, 1, 2)
        
        # Hàng 2: Học sinh - Ô hiển thị và nút chọn
        label_students = QLabel('Học sinh')
        label_students.setFont(QFont("Arial", 14))
        label_students.setStyleSheet("background: transparent; border: none;")
        self.students_line = QLineEdit()
        self.students_line.setPlaceholderText("Chưa chọn học sinh")
        self.students_line.setReadOnly(True)
        self.students_line.setFixedHeight(30)
        self.btn_select_students = QPushButton("Chọn học sinh")
        self.btn_select_students.setFixedSize(150, 35)
        self.btn_select_students.clicked.connect(self.open_student_selector)
        students_layout = QHBoxLayout()
        students_layout.addWidget(self.students_line)
        students_layout.addWidget(self.btn_select_students)
        form_layout.addWidget(label_students, 2, 0)
        form_layout.addLayout(students_layout, 2, 1)
        
        # Hàng 3: Giáo viên - Ô hiển thị và nút chọn (chỉ cho phép chọn 1)
        label_teacher = QLabel('Giáo viên <span style="color:red; font-size:16px;">*</span>')
        label_teacher.setFont(QFont("Arial", 14))
        label_teacher.setStyleSheet("background: transparent; border: none;")
        self.teacher_line = QLineEdit()
        self.teacher_line.setPlaceholderText("Chưa chọn giáo viên")
        self.teacher_line.setReadOnly(True)
        self.teacher_line.setFixedHeight(30)
        self.btn_select_teacher = QPushButton("Chọn giáo viên")
        self.btn_select_teacher.setFixedSize(150, 35)
        self.btn_select_teacher.clicked.connect(self.open_teacher_selector)
        teacher_layout = QHBoxLayout()
        teacher_layout.addWidget(self.teacher_line)
        teacher_layout.addWidget(self.btn_select_teacher)
        form_layout.addWidget(label_teacher, 3, 0)
        form_layout.addLayout(teacher_layout, 3, 1)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        
        # Nút thêm lớp (căn phải)
        self.add_button = QPushButton("Thêm lớp học")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        self.add_button.setEnabled(False)
        self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px;")
        self.add_button.clicked.connect(self.add_class)
        main_layout.addWidget(self.add_button, alignment=Qt.AlignRight)
        
        # Kiểm tra điều kiện: tên lớp và giáo viên phải được nhập/chọn
        self.class_name_input.textChanged.connect(self.check_input)
    
    def check_input(self):
        if self.class_name_input.text().strip() and self.selected_teacher:
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white; border: none; border-radius: 8px;")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border: none; border-radius: 8px;")
    
    def open_student_selector(self):
        dialog = StudentSelectorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.get_selection()  # trả về danh sách các dòng (mỗi dòng là list)
            if selected:
                # Giả sử hiển thị cột "Tên học sinh" (index 1)
                names = [row[1] for row in selected]
                self.selected_students = names
                self.students_line.setText(", ".join(names))
            else:
                self.students_line.setText("Chưa chọn học sinh")
    
    def open_teacher_selector(self):
        dialog = TeacherSelectorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected = dialog.get_selection()  # trả về một list cho dòng được chọn
            if selected:
                # Giả sử hiển thị cột "Tên giáo viên" (index 1)
                self.selected_teacher = selected[1]
                self.teacher_line.setText(self.selected_teacher)
            else:
                self.teacher_line.setText("Chưa chọn giáo viên")
            self.check_input()
    
    def add_class(self):
        class_name = self.class_name_input.text().strip()
        teacher = self.selected_teacher
        students = self.selected_students
        print(f"Thêm lớp: {class_name}, Giáo viên: {teacher}, Học sinh: {students}")
        self.show_notification()
    
    def show_notification(self):
        notif = QDialog(self, flags=Qt.FramelessWindowHint)
        notif.setModal(True)
        notif.setAttribute(Qt.WA_TranslucentBackground)
        notif.resize(self.size())
        
        frame = QFrame(notif)
        frame.setStyleSheet("background-color: #28a745; border-radius: 8px;")
        frame.setFixedSize(300, 60)
        frame.move((notif.width() - frame.width()) // 2, (notif.height() - frame.height()) // 2)
        
        label = QLabel("Thêm lớp học thành công", frame)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        label.resize(frame.size())
        
        notif.show()
        QTimer.singleShot(2000, notif.accept)
    
    def go_back(self):
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(CLASS_PAGE_ID)
        else:
            print("Parent stack chưa được cung cấp.")
