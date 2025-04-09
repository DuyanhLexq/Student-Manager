from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QGridLayout, QDialog, QFrame
)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt, QDate, QTimer,QSize
from GUI.config import BACK_ICON_PATH,STUDENT_PAGE_ID
from GUI.util import get_right_table_data_form
from GUI.notification import FloatingNotification
from functions.functions import get_preview_data
from sqlQuery import GET_STUDENT_INFO_BY_ID_QUERY
from datetime import datetime

class AlterStudentPage(QWidget):
    def __init__(self, parent_stack=None, student_id = None):
        """
        parent_stack: QStackedWidget chứa các trang của ứng dụng,
                      dùng để chuyển trang quay lại.
        """
        super().__init__()
        self.parent_stack = parent_stack
        self.student_data = get_right_table_data_form(get_preview_data(GET_STUDENT_INFO_BY_ID_QUERY.format(student_id)))[0] if student_id else None
        self.initUI()
        
    def initUI(self):
        # Thiết lập font chung cho toàn bộ form
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
        
        # Sử dụng QGridLayout cho form nhập
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(15)
        
        # Hàng 1: Tên Học sinh (*) và Giới tính (*)
        label_name = QLabel('Tên Học sinh')
        label_name.setFont(QFont("Arial", 14))
        label_name.setStyleSheet("background: transparent; border: none;")
        self.name_input = QLineEdit()
        self.name_input.setText(self.student_data[0] if self.student_data else "")
        self.name_input.setFixedHeight(30)
        
        label_gender = QLabel('Giới tính')
        label_gender.setFont(QFont("Arial", 14))
        label_gender.setStyleSheet("background: transparent; border: none;")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Nam", "Nữ"])
        self.gender_combo.setCurrentText(self.student_data[1] if self.student_data else "Nam")
        self.gender_combo.setFixedHeight(30)
        
        form_layout.addWidget(label_name, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(label_gender, 0, 2)
        form_layout.addWidget(self.gender_combo, 0, 3)
        
        # Hàng 2: Ngày tháng năm sinh (*)
        label_dob = QLabel('Ngày tháng năm sinh')
        label_dob.setFont(QFont("Arial", 14))
        label_dob.setStyleSheet("background: transparent; border: none;")
        self.dob_edit = QDateEdit()
        self.dob_edit.setDisplayFormat("dd/MM/yyyy")
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setFixedHeight(30)
        parsed_date = datetime.strptime(self.student_data[2], "%Y-%m-%d").date()  # => datetime.date
        qdate = QDate(parsed_date.year, parsed_date.month, parsed_date.day)
        self.dob_edit.setDate(qdate if self.student_data else QDate.currentDate())
        
        
        form_layout.addWidget(label_dob, 1, 0, 1, 1)
        form_layout.addWidget(self.dob_edit, 1, 1, 1, 3)
        
        # Hàng 3: Quê Quán (*)
        label_hometown = QLabel('Quê Quán')
        label_hometown.setFont(QFont("Arial", 14))
        label_hometown.setStyleSheet("background: transparent; border: none;")
        self.hometown_input = QLineEdit()
        self.hometown_input.setText(self.student_data[3] if self.student_data else "")
        self.hometown_input.setFixedHeight(30)
        
        form_layout.addWidget(label_hometown, 2, 0)
        form_layout.addWidget(self.hometown_input, 2, 1, 1, 3)
        
        # Hàng 4: Tạm trú (*)
        label_residence = QLabel('Tạm trú')
        label_residence.setFont(QFont("Arial", 14))
        label_residence.setStyleSheet("background: transparent; border: none;")
        self.residence_input = QLineEdit()
        self.residence_input.setText(self.student_data[4] if self.student_data else "")
        self.residence_input.setFixedHeight(30)
        
        form_layout.addWidget(label_residence, 3, 0)
        form_layout.addWidget(self.residence_input, 3, 1, 1, 3)
        
        # Hàng 5: Họ tên bố (*) và Họ tên mẹ (*)
        label_parent = QLabel('Họ tên phụ huynh')
        label_parent.setFont(QFont("Arial", 14))
        label_parent.setStyleSheet("background: transparent; border: none;")
        self.parent_input = QLineEdit()
        self.parent_input.setText(self.student_data[5] if self.student_data else "")
        self.parent_input.setFixedHeight(30)
        
        form_layout.addWidget(label_parent, 4, 0)
        form_layout.addWidget(self.parent_input, 4, 1)
        
        # Hàng 6: Số điện thoại (không bắt buộc) và Số điện thoại phụ huynh (không bắt buộc)
        label_phone = QLabel("Số điện thoại")
        label_phone.setFont(QFont("Arial", 14))
        label_phone.setStyleSheet("background: transparent; border: none;")
        self.phone_input = QLineEdit()
        self.phone_input.setText(self.student_data[6] if self.student_data else "")
        self.phone_input.setFixedHeight(30)
        
        label_parent_phone = QLabel("Số điện thoại phụ huynh")
        label_parent_phone.setFont(QFont("Arial", 14))
        label_parent_phone.setStyleSheet("background: transparent; border: none;")
        self.parent_phone_input = QLineEdit()
        self.parent_phone_input.setText(self.student_data[7] if self.student_data else "")
        self.parent_phone_input.setFixedHeight(30)
        
        form_layout.addWidget(label_phone, 5, 0)
        form_layout.addWidget(self.phone_input, 5, 1)
        form_layout.addWidget(label_parent_phone, 5, 2)
        form_layout.addWidget(self.parent_phone_input, 5, 3)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        
        # Bottom layout: Nút "Thêm học sinh" bên phải dưới cùng
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.add_button = QPushButton("Sửa học sinh")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        # Ban đầu disabled, màu xám
        self.add_button.setEnabled(True)
        self.add_button.setStyleSheet("background-color: #007BFF; color: white;border-radius: 8px")
        bottom_layout.addWidget(self.add_button)
        main_layout.addLayout(bottom_layout)
        
        # Kết nối sự kiện: kiểm tra các ô bắt buộc để bật/tắt nút
        self.name_input.textChanged.connect(self.check_input)
        self.hometown_input.textChanged.connect(self.check_input)
        self.residence_input.textChanged.connect(self.check_input)
        self.parent_input.textChanged.connect(self.check_input)
        
        # Nút Thêm được kết nối sự kiện
        self.add_button.clicked.connect(self.add_student)

        for btn in [self.back_button, self.add_button]:
            btn.setCursor(Qt.PointingHandCursor)
    
    def check_input(self):
        # Các ô bắt buộc: Tên học sinh, Quê Quán, Tạm trú, Họ tên bố, Họ tên mẹ
        if (self.name_input.text().strip() and
            self.hometown_input.text().strip() and
            self.residence_input.text().strip() and
            self.parent_input.text().strip()):
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white; border: none;")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border: none;")
    
    def add_student(self):
        # Lấy thông tin từ các ô nhập
        name = self.name_input.text().strip()
        gender = self.gender_combo.currentText()
        dob = self.dob_edit.date().toString("dd/MM/yyyy")
        hometown = self.hometown_input.text().strip()
        residence = self.residence_input.text().strip()
        parent = self.parent_input.text().strip()
        phone = self.phone_input.text().strip()
        parent_phone = self.parent_phone_input.text().strip()
        
        print(f"Thêm học sinh: {name}, {gender}, {dob}, {hometown}, {residence}, {parent}, {phone}, {parent_phone}")
        self.show_notification()
    
    def show_notification(self):
        notif = FloatingNotification(
            "Sửa học sinh thành công!",
            parent=self.parent_stack,
            bg_color="#28a745",  # Màu xanh lá
            icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
        )
        notif.show_bottom_center()
    
    def go_back(self):
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(STUDENT_PAGE_ID)
