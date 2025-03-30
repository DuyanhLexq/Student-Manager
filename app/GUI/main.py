import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    QStackedWidget, QFrame
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

from home import HomePage
from student import StudentPage
from teacher import TeacherPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản Lý Trung Tâm Toán")
        self.resize(1000, 600)
        self.initUI()
        self.loadStyleSheet()

    def initUI(self):
        # Widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Khung menu bên trái
        self.menu_frame = QFrame()
        self.menu_frame.setObjectName("MenuFrame")
        self.menu_frame.setFixedWidth(220)

        menu_layout = QVBoxLayout(self.menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(10)
        menu_layout.setAlignment(Qt.AlignTop)

        # Icon user
        from PyQt5.QtWidgets import QLabel  # Import tại đây để dùng cho icon
        user_icon_label = QLabel()
        user_icon_label.setObjectName("UserIcon")
        pixmap = QPixmap("user.png")
        pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        user_icon_label.setPixmap(pixmap)
        user_icon_label.setAlignment(Qt.AlignCenter)
        menu_layout.addWidget(user_icon_label)

        # Các nút menu
        self.btn_home = QPushButton("Trang chủ")
        self.btn_students = QPushButton("Học sinh")
        self.btn_teachers = QPushButton("Giáo viên")
        for btn in [self.btn_home, self.btn_students, self.btn_teachers]:
            btn.setObjectName("MenuButton")
            btn.setFixedHeight(40)
            btn.setFont(QFont("Arial", 12))
            menu_layout.addWidget(btn)
        menu_layout.addStretch()

        # Khu vực nội dung bên phải (QStackedWidget)
        self.stack = QStackedWidget()
        self.stack.setObjectName("StackedWidget")

        # Các trang được định nghĩa riêng:
        self.home_page = HomePage()        # File home.py
        self.student_page = StudentPage()  # File student.py
        self.teacher_page = TeacherPage()  # File teacher.py

        self.stack.addWidget(self.home_page)      # index 0
        self.stack.addWidget(self.student_page)   # index 1
        self.stack.addWidget(self.teacher_page)   # index 2

        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(self.stack)

        # Kết nối sự kiện cho các nút menu
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_students.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_teachers.clicked.connect(lambda: self.stack.setCurrentIndex(2))

    def loadStyleSheet(self):
        try:
            with open(r"C:\Project_Python\applications\Student-Manager\app\GUI\style.css", "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception as e:
            print("Không load được file style.qss:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
