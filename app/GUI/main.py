import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QFrame, QLabel
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from GUI.home import HomePage
from GUI.student import StudentPage
from GUI.teacher import TeacherPage
from GUI.config import TEACHER_ICON_PATH, HOME_ICON_PATH, STUDENT_ICON_PATH
from GUI.util import convert_icon_to_white

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Trung Tâm Toán")
        self.resize(1000, 600)
        self.initUI()
        self.loadStyleSheet()
        # Danh sách chứa các nút menu cần active style
        self.all_menu_buttons = [
            self.btn_home,
            self.btn_students,
            self.btn_manage_students,
            self.btn_manage_grades,
            self.btn_manage_fees,
            self.btn_teacher,
            self.btn_manage_teacher,
            self.btn_teacher_salary
        ]

    def initUI(self):
        # Widget trung tâm và layout chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Khung menu bên trái (objectName "MenuFrame" để CSS áp dụng)
        self.menu_frame = QFrame()
        self.menu_frame.setObjectName("MenuFrame")
        self.menu_frame.setFixedWidth(220)
        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(10)
        menu_layout.setAlignment(Qt.AlignTop)
        
        # Icon user
        user_icon_label = QLabel()
        user_icon_label.setObjectName("UserIcon")
        pixmap = QPixmap("user.png")
        pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        user_icon_label.setPixmap(pixmap)
        user_icon_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(user_icon_label)

        # Nút Trang chủ
        self.btn_home = QPushButton("Trang chủ")
        self.btn_home.setObjectName("MenuButton")
        self.btn_home.setIcon(QIcon(convert_icon_to_white(HOME_ICON_PATH)))
        self.btn_home.setFixedHeight(40)
        self.btn_home.setFont(QFont("Arial", 14))
        self.btn_home.setStyleSheet("color: #FFFFFF; background: transparent; border: none; text-align: left; padding-left: 20px;")
        menu_layout.addWidget(self.btn_home)

        # Nút Học sinh
        self.btn_students = QPushButton("Học sinh")
        self.btn_students.setObjectName("MenuButton")
        self.btn_students.setIcon(QIcon(convert_icon_to_white(STUDENT_ICON_PATH)))
        self.btn_students.setCheckable(True)
        self.btn_students.setFixedHeight(40)
        self.btn_students.setFont(QFont("Arial", 14))
        self.btn_students.setStyleSheet("color: #FFFFFF; background: transparent; border: none; text-align: left; padding-left: 20px;")
        menu_layout.addWidget(self.btn_students)

        # Widget chứa submenu của Học sinh (thụt vào)
        self.submenu_students = QWidget()
        submenu_layout = QVBoxLayout(self.submenu_students)
        submenu_layout.setContentsMargins(40, 0, 0, 0)  # Thụt vào để thể hiện quan hệ
        submenu_layout.setSpacing(5)
        self.btn_manage_students = QPushButton("Quản lý học sinh")
        self.btn_manage_grades = QPushButton("Quản lý điểm")
        self.btn_manage_fees = QPushButton("Học phí")
        for btn in [self.btn_manage_students, self.btn_manage_grades, self.btn_manage_fees]:
            btn.setObjectName("SubMenuButton")
            btn.setFont(QFont("Arial", 13))
            btn.setFixedHeight(30)
            btn.setStyleSheet("color: #FFFFFF; background: transparent; border: none; text-align: left;")
            submenu_layout.addWidget(btn)
        self.submenu_students.hide()  # Ẩn submenu ban đầu
        menu_layout.addWidget(self.submenu_students)

        # Nút Giáo viên
        self.btn_teacher = QPushButton("Giáo viên")
        self.btn_teacher.setObjectName("MenuButton")
        self.btn_teacher.setIcon(QIcon(convert_icon_to_white(TEACHER_ICON_PATH)))
        self.btn_teacher.setCheckable(True)
        self.btn_teacher.setFixedHeight(40)
        self.btn_teacher.setFont(QFont("Arial", 14))
        self.btn_teacher.setStyleSheet("color: #FFFFFF; background: transparent; border: none; text-align: left; padding-left: 20px;")
        menu_layout.addWidget(self.btn_teacher)

        # Widget chứa submenu của Giáo viên (thụt vào)
        self.submenu_teacher = QWidget()
        teacher_sub_layout = QVBoxLayout(self.submenu_teacher)
        teacher_sub_layout.setContentsMargins(40, 0, 0, 0)  # Thụt vào
        teacher_sub_layout.setSpacing(5)
        self.btn_manage_teacher = QPushButton("Quản lý giáo viên")
        self.btn_teacher_salary = QPushButton("Lương")
        for btn in [self.btn_manage_teacher, self.btn_teacher_salary]:
            btn.setObjectName("SubMenuButton")
            btn.setFont(QFont("Arial", 13))
            btn.setFixedHeight(30)
            btn.setStyleSheet("color: #FFFFFF; background: transparent; border: none; text-align: left;")
            teacher_sub_layout.addWidget(btn)
        self.submenu_teacher.hide()  # Ẩn submenu ban đầu
        menu_layout.addWidget(self.submenu_teacher)

        menu_layout.addStretch()

        # Khu vực nội dung bên phải (QStackedWidget)
        self.stack = QStackedWidget()
        self.stack.setObjectName("StackedWidget")

        # Các trang nội dung
        self.home_page = HomePage()
        self.student_page = StudentPage(main_stack=self.stack)
        self.grade_page = QWidget()  # Placeholder cho quản lý điểm
        grade_layout = QVBoxLayout(self.grade_page)
        grade_label = QLabel("Quản lý điểm")
        grade_label.setFont(QFont("Arial", 16))
        grade_layout.addWidget(grade_label)
        grade_layout.addStretch()
        self.fee_page = QWidget()  # Placeholder cho học phí
        fee_layout = QVBoxLayout(self.fee_page)
        fee_label = QLabel("Học phí")
        fee_label.setFont(QFont("Arial", 16))
        fee_layout.addWidget(fee_label)
        fee_layout.addStretch()
        self.teacher_page = TeacherPage(main_stack=self.stack)
        self.teacher_salary_page = QWidget()  # Placeholder cho quản lý lương
        teacher_salary_layout = QVBoxLayout(self.teacher_salary_page)
        teacher_salary_label = QLabel("Lương")
        teacher_salary_label.setFont(QFont("Arial", 16))
        teacher_salary_layout.addWidget(teacher_salary_label)
        teacher_salary_layout.addStretch()

        self.stack.addWidget(self.home_page)         # index 0
        self.stack.addWidget(self.student_page)      # index 1
        self.stack.addWidget(self.grade_page)          # index 2
        self.stack.addWidget(self.fee_page)            # index 3
        self.stack.addWidget(self.teacher_page)        # index 4
        self.stack.addWidget(self.teacher_salary_page) # index 5

        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(self.stack)

        # Kết nối sự kiện cho các nút menu và submenu
        self.btn_home.clicked.connect(lambda: self.switch_page(self.home_page, self.btn_home))
        self.btn_students.clicked.connect(lambda: self.toggle_students_menu())
        self.btn_manage_students.clicked.connect(lambda: self.switch_page(self.student_page, self.btn_manage_students))
        self.btn_manage_grades.clicked.connect(lambda: self.switch_page(self.grade_page, self.btn_manage_grades))
        self.btn_manage_fees.clicked.connect(lambda: self.switch_page(self.fee_page, self.btn_manage_fees))
        self.btn_teacher.clicked.connect(lambda: self.toggle_teacher_menu())
        self.btn_manage_teacher.clicked.connect(lambda: self.switch_page(self.teacher_page, self.btn_manage_teacher))
        self.btn_teacher_salary.clicked.connect(lambda: self.switch_page(self.teacher_salary_page, self.btn_teacher_salary))

    def clear_active_styles(self):
        for btn in self.all_menu_buttons:
            btn.setStyleSheet("color: #FFFFFF; background: transparent; font-weight: normal; text-align: left; padding-left: 20px;")

    def set_active_button(self, btn):
        self.clear_active_styles()
        # Active style: nền khác (#1F2A36) và chữ in đậm
        btn.setStyleSheet("color: #FFFFFF; background-color: #1F2A36; text-align: left; padding-left: 20px;")

    def switch_page(self, page, btn):
        self.stack.setCurrentWidget(page)
        self.set_active_button(btn)

    def toggle_students_menu(self):
        if self.submenu_students.isVisible():
            self.submenu_students.hide()
            self.btn_students.setChecked(False)
            self.set_active_button(self.btn_students)
        else:
            self.submenu_students.show()
            self.btn_students.setChecked(True)
            self.set_active_button(self.btn_students)

    def toggle_teacher_menu(self):
        if self.submenu_teacher.isVisible():
            self.submenu_teacher.hide()
            self.btn_teacher.setChecked(False)
            self.set_active_button(self.btn_teacher)
        else:
            self.submenu_teacher.show()
            self.btn_teacher.setChecked(True)
            self.set_active_button(self.btn_teacher)

    def loadStyleSheet(self):
        try:
            with open("app/GUI/style.css", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception as e:
            print("Không load được file style.qss:", e)

def Run():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

