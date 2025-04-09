# File: addTeacher_func.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QDateEdit, QDialog, QFrame
)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt, QDate, QTimer,QSize
from GUI.config import BACK_ICON_PATH,TEACHER_PAGE_ID
from functions.functions import add_new_teacher

class AddTeacherPage(QWidget):
    def __init__(self, parent_stack=None):
        super().__init__()
        self.parent_stack = parent_stack
        self.initUI()
        
    def initUI(self):
        # Thiết lập font chung cho toàn bộ form
        self.setFont(QFont("Arial", 14))
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
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
        layout.addLayout(top_layout)
        
        # Row 1: Tên Giáo viên (*)  
        row1 = QHBoxLayout()
        label_name = QLabel('Tên Giáo viên <span style="color:red; font-size:16px;">*</span>')
        label_name.setFont(QFont("Arial", 14))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên giáo viên")
        self.name_input.setFixedHeight(30)
        row1.addWidget(label_name)
        row1.addWidget(self.name_input)
        layout.addLayout(row1)
        
        # Row 2: Ngày tháng năm sinh (*)
        row2 = QHBoxLayout()
        label_dob = QLabel('Ngày tháng năm sinh <span style="color:red; font-size:16px;">*</span>')
        label_dob.setFont(QFont("Arial", 14))
        self.dob_edit = QDateEdit()
        self.dob_edit.setDisplayFormat("dd/MM/yyyy")
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setFixedHeight(30)
        self.dob_edit.setDate(QDate.currentDate())
        row2.addWidget(label_dob)
        row2.addWidget(self.dob_edit)
        layout.addLayout(row2)
        
        # Row 3: Số điện thoại (không bắt buộc)
        row3 = QHBoxLayout()
        label_phone = QLabel("Số điện thoại")
        label_phone.setFont(QFont("Arial", 14))
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Nhập số điện thoại")
        self.phone_input.setFixedHeight(30)
        row3.addWidget(label_phone)
        row3.addWidget(self.phone_input)
        layout.addLayout(row3)
        
        # Row 4: Ngày hết hạn hợp đồng (*) và Lương (*)
        row4 = QHBoxLayout()
        label_contract = QLabel('Ngày hết hạn hợp đồng <span style="color:red; font-size:16px;">*</span>')
        label_contract.setFont(QFont("Arial", 14))
        self.contract_edit = QDateEdit()
        self.contract_edit.setDisplayFormat("dd/MM/yyyy")
        self.contract_edit.setCalendarPopup(True)
        self.contract_edit.setFixedHeight(30)
        label_hometown = QLabel('Quê quán <span style="color:red; font-size:16px;">*</span>')
        label_hometown.setFont(QFont("Arial", 14))
        self.hometown_input = QLineEdit()
        self.hometown_input.setPlaceholderText("Nhập quê quán")
        self.hometown_input.setFixedHeight(30)
        row4.addWidget(label_hometown)
        row4.addWidget(self.hometown_input)
        layout.addLayout(row4)
        
        
        # Row 5: Ngày vào nhận việc (*)
        row5 = QHBoxLayout()
        label_start = QLabel('Ngày vào nhận việc <span style="color:red; font-size:16px;">*</span>')
        label_start.setFont(QFont("Arial", 14))
        self.start_date = QDateEdit()
        self.start_date.setDisplayFormat("dd/MM/yyyy")
        self.start_date.setCalendarPopup(True)
        self.start_date.setFixedHeight(30)
        self.start_date.setDate(QDate.currentDate())
        row5.addWidget(label_start)
        row5.addWidget(self.start_date)
        layout.addLayout(row5)
        
        layout.addStretch()
        
        # Bottom layout: Nút "Thêm giáo viên"
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        self.add_button = QPushButton("Thêm giáo viên")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        self.add_button.setEnabled(False)
        self.add_button.setStyleSheet("background-color: #A9A9A9; color: white;border-radius: 8px")
        bottom_layout.addWidget(self.add_button)
        layout.addLayout(bottom_layout)
        
        # Kết nối sự kiện để kiểm tra các trường bắt buộc
        self.name_input.textChanged.connect(self.check_input)
        self.contract_edit.dateChanged.connect(self.check_input)
        self.hometown_input.textChanged.connect(self.check_input)
        self.start_date.dateChanged.connect(self.check_input)
        self.add_button.clicked.connect(self.add_teacher)

        for btn in [self.back_button, self.add_button]:
            btn.setCursor(Qt.PointingHandCursor)
    
    def check_input(self):
        # Các trường bắt buộc: Tên, Ngày hết hạn hợp đồng, Lương, Ngày vào nhận việc
        if self.name_input.text().strip() and self.hometown_input.text().strip():
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white;border-radius: 8px")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white;border-radius: 8px")
    
    def add_teacher(self):
        name = self.name_input.text().strip()
        dob = self.dob_edit.date().toString("dd/MM/yyyy")
        phone = self.phone_input.text().strip()
        contract = self.contract_edit.date().toString("dd/MM/yyyy")
        hometown = self.hometown_input.text().strip()
        start = self.start_date.date().toString("dd/MM/yyyy")
        data = [
            name,
            phone,
            hometown,
            start,
            contract,
            dob
        ]
        add_new_teacher(data)
        print(f"Thêm giáo viên: {name}, {dob}, {phone}, {contract}, {hometown}, {start}")
        self.show_notification()
    
    def show_notification(self):
        from PyQt5.QtCore import QTimer
        notif = QDialog(self, flags=Qt.FramelessWindowHint)
        notif.setModal(True)
        notif.setAttribute(Qt.WA_TranslucentBackground)
        notif.setStyleSheet("background: transparent; border: none;")
        notif.resize(self.size())
        
        frame = QFrame(notif)
        frame.setStyleSheet("background-color: #28a745; border-radius: 8px; border: none;")
        frame.setFixedSize(300, 60)
        frame.move((notif.width()-frame.width())//2, (notif.height()-frame.height())//2)
        
        label = QLabel("Thêm giáo viên thành công", frame)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: white; background: transparent; border: none;")
        label.setAlignment(Qt.AlignCenter)
        label.resize(frame.size())
        
        notif.show()
        QTimer.singleShot(2000, notif.accept)
    
    def go_back(self):
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(TEACHER_PAGE_ID)

