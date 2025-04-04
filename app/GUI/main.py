import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QFrame, QLabel, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
from GUI.home import HomePage
from GUI.Student.student import StudentPage, GradesPage, TuitionPage
from GUI.Teacher.teacher import TeacherPage, SalaryPage
from GUI.config import (TEACHER_ICON_PATH,
                        HOME_ICON_PATH, STUDENT_ICON_PATH, CLASS_ICON_PATH,
                        SETTING_ICON_PATH, DATABASE_ICON_PATH, ACCOUNT_ICON_PATH)
from GUI.util import convert_icon_to_white,get_rounded_pixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Trung Tâm Toán")
        self.resize(1000, 600)
        self.initUI()
        self.loadStyleSheet()
        # Tập hợp các nút menu để active style chung
        self.all_menu_buttons = [
            self.btn_home,
            self.btn_students,
            self.btn_manage_students,
            self.btn_manage_grades,
            self.btn_manage_fees,
            self.btn_teacher,
            self.btn_manage_teacher,
            self.btn_teacher_salary,
            self.btn_class_management,
            self.btn_data,
            self.btn_account,
            self.btn_settings
        ]

    def initUI(self):
        # Widget trung tâm và layout chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Khung menu bên trái với style hiện đại
        self.menu_frame = QFrame()
        self.menu_frame.setObjectName("MenuFrame")
        self.menu_frame.setFixedWidth(220)
        menu_layout = QVBoxLayout(self.menu_frame)
        # Điều chỉnh margin dưới để các mục đẩy xuống một chút
        menu_layout.setContentsMargins(0, 20, 0, 10)
        menu_layout.setSpacing(15)
        menu_layout.setAlignment(Qt.AlignTop)
        
        # Icon user (ở đầu menu)
        user_icon_label = QLabel()
        user_icon_label.setObjectName("UserIcon")
        pixmap = QPixmap(r"C:\Project_Python\applications\Student-Manager\app\assets\user.jpg")
        if not pixmap.isNull():
            # Tạo pixmap hình tròn với đường kính 80 (80/2 = 40 là bán kính)
            rounded_pixmap = get_rounded_pixmap(pixmap, 80)
            user_icon_label.setPixmap(rounded_pixmap)
        else:
            print("Không tải được ảnh user.jpg")
        user_icon_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(user_icon_label)
        # Nút menu chính
        self.btn_home = self.create_menu_button("Trang chủ", HOME_ICON_PATH)
        menu_layout.addWidget(self.btn_home)
        
        self.btn_students = self.create_menu_button("Học sinh", STUDENT_ICON_PATH, checkable=True)
        menu_layout.addWidget(self.btn_students)
        
        # Submenu Học sinh
        self.submenu_students = QWidget()
        submenu_layout = QVBoxLayout(self.submenu_students)
        submenu_layout.setContentsMargins(40, 0, 0, 0)
        submenu_layout.setSpacing(5)
        self.btn_manage_students = self.create_submenu_button("Quản lý học sinh")
        self.btn_manage_grades   = self.create_submenu_button("Quản lý điểm")
        self.btn_manage_fees     = self.create_submenu_button("Học phí")
        for btn in [self.btn_manage_students, self.btn_manage_grades, self.btn_manage_fees]:
            submenu_layout.addWidget(btn)
        self.submenu_students.hide()
        menu_layout.addWidget(self.submenu_students)
        
        self.btn_teacher = self.create_menu_button("Giáo viên", TEACHER_ICON_PATH, checkable=True)
        menu_layout.addWidget(self.btn_teacher)
        
        # Submenu Giáo viên
        self.submenu_teacher = QWidget()
        teacher_sub_layout = QVBoxLayout(self.submenu_teacher)
        teacher_sub_layout.setContentsMargins(40, 0, 0, 0)
        teacher_sub_layout.setSpacing(5)
        self.btn_manage_teacher = self.create_submenu_button("Quản lý giáo viên")
        self.btn_teacher_salary   = self.create_submenu_button("Lương")
        for btn in [self.btn_manage_teacher, self.btn_teacher_salary]:
            teacher_sub_layout.addWidget(btn)
        self.submenu_teacher.hide()
        menu_layout.addWidget(self.submenu_teacher)
        
        # Các mục menu chính khác
        self.btn_class_management = self.create_menu_button("Quản lý lớp", CLASS_ICON_PATH)
        menu_layout.addWidget(self.btn_class_management)
        
        # Thêm stretch để đẩy các mục dưới cùng xuống dưới
        menu_layout.addStretch()
        
        self.btn_data = self.create_menu_button("Dữ liệu", DATABASE_ICON_PATH)
        menu_layout.addWidget(self.btn_data)

        self.btn_account = self.create_menu_button("Tài khoản", ACCOUNT_ICON_PATH)
        menu_layout.addWidget(self.btn_account)

        self.btn_settings = self.create_menu_button("Cài đặt", SETTING_ICON_PATH)
        menu_layout.addWidget(self.btn_settings)

        # Khu vực nội dung bên phải (QStackedWidget)
        self.stack = QStackedWidget()
        self.stack.setObjectName("StackedWidget")
        
        # Các trang nội dung
        self.home_page = HomePage()
        self.student_page = StudentPage(main_stack=self.stack)
        self.grade_page = GradesPage(main_stack=self.stack)
        self.fee_page = TuitionPage(main_stack=self.stack)
        self.teacher_page = TeacherPage(main_stack=self.stack)
        self.teacher_salary_page = SalaryPage(main_stack=self.stack)
        self.class_management_page = QWidget()
        self.settings_page = QWidget()
        self.data_page = QWidget()
        self.account_page = QWidget()
        
        self.stack.addWidget(self.home_page)              # index 0
        self.stack.addWidget(self.student_page)           # index 1
        self.stack.addWidget(self.grade_page)             # index 2
        self.stack.addWidget(self.fee_page)               # index 3
        self.stack.addWidget(self.teacher_page)           # index 4
        self.stack.addWidget(self.teacher_salary_page)    # index 5
        self.stack.addWidget(self.class_management_page)  # index 6
        self.stack.addWidget(self.data_page)              # index 7
        self.stack.addWidget(self.account_page)           # index 8
        self.stack.addWidget(self.settings_page)          # index 9
        
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
        
        self.btn_class_management.clicked.connect(lambda: self.switch_page(self.class_management_page, self.btn_class_management))
        self.btn_data.clicked.connect(lambda: self.switch_page(self.data_page, self.btn_data))
        self.btn_account.clicked.connect(lambda: self.switch_page(self.account_page, self.btn_account))
        self.btn_settings.clicked.connect(lambda: self.switch_page(self.settings_page, self.btn_settings))
        
    def create_menu_button(self, text, icon_path=None, checkable=False):
        btn = QPushButton(text)
        btn.setObjectName("MenuButton")
        btn.setFixedHeight(40)
        btn.setFont(QFont("Arial", 14))
        btn.setCursor(Qt.PointingHandCursor)
        if icon_path:
            btn.setIcon(QIcon(convert_icon_to_white(icon_path)))
        btn.setCheckable(checkable)
        btn.setStyleSheet(
            "color: #FFFFFF; background: transparent; border: none; "
            "text-align: left; padding-left: 20px;"
        )
        return btn

    def create_submenu_button(self, text):
        btn = QPushButton(text)
        btn.setObjectName("SubMenuButton")
        btn.setFixedHeight(30)
        btn.setFont(QFont("Arial", 13))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(
            "color: #FFFFFF; background: transparent; border: none; text-align: left;"
        )
        return btn

    def clear_active_styles(self):
        for btn in self.all_menu_buttons:
            btn.setStyleSheet(
                "color: #FFFFFF; background: transparent; font-weight: normal; "
                "text-align: left; padding-left: 20px;"
            )

    def set_active_button(self, btn):
        self.clear_active_styles()
        btn.setStyleSheet(
            "color: #FFFFFF; background-color: #1F2A36; text-align: left; padding-left: 20px;"
        )

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