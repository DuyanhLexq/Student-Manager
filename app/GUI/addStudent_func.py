from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QDateEdit, QGridLayout, QDialog, QFrame
)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt, QDate, QTimer,QSize
from GUI.config import BACK_ICON_PATH

class AddStudentPage(QWidget):
    def __init__(self, parent_stack=None):
        """
        parent_stack: QStackedWidget chứa các trang của ứng dụng,
                      dùng để chuyển trang quay lại.
        """
        super().__init__()
        self.parent_stack = parent_stack
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
        label_name = QLabel('Tên Học sinh <span style="color:red; font-size:16px;">*</span>')
        label_name.setFont(QFont("Arial", 14))
        label_name.setStyleSheet("background: transparent; border: none;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên học sinh")
        self.name_input.setFixedHeight(30)
        
        label_gender = QLabel('Giới tính <span style="color:red; font-size:16px;">*</span>')
        label_gender.setFont(QFont("Arial", 14))
        label_gender.setStyleSheet("background: transparent; border: none;")
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Nam", "Nữ"])
        self.gender_combo.setFixedHeight(30)
        
        form_layout.addWidget(label_name, 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(label_gender, 0, 2)
        form_layout.addWidget(self.gender_combo, 0, 3)
        
        # Hàng 2: Ngày tháng năm sinh (*)
        label_dob = QLabel('Ngày tháng năm sinh <span style="color:red; font-size:16px;">*</span>')
        label_dob.setFont(QFont("Arial", 14))
        label_dob.setStyleSheet("background: transparent; border: none;")
        self.dob_edit = QDateEdit()
        self.dob_edit.setDisplayFormat("dd/MM/yyyy")
        self.dob_edit.setCalendarPopup(True)
        self.dob_edit.setFixedHeight(30)
        self.dob_edit.setDate(QDate.currentDate())
        
        
        form_layout.addWidget(label_dob, 1, 0, 1, 1)
        form_layout.addWidget(self.dob_edit, 1, 1, 1, 3)
        
        # Hàng 3: Quê Quán (*)
        label_hometown = QLabel('Quê Quán <span style="color:red; font-size:16px;">*</span>')
        label_hometown.setFont(QFont("Arial", 14))
        label_hometown.setStyleSheet("background: transparent; border: none;")
        self.hometown_input = QLineEdit()
        self.hometown_input.setPlaceholderText("Nhập quê quán")
        self.hometown_input.setFixedHeight(30)
        
        form_layout.addWidget(label_hometown, 2, 0)
        form_layout.addWidget(self.hometown_input, 2, 1, 1, 3)
        
        # Hàng 4: Tạm trú (*)
        label_residence = QLabel('Tạm trú <span style="color:red; font-size:16px;">*</span>')
        label_residence.setFont(QFont("Arial", 14))
        label_residence.setStyleSheet("background: transparent; border: none;")
        self.residence_input = QLineEdit()
        self.residence_input.setPlaceholderText("Nhập nơi tạm trú")
        self.residence_input.setFixedHeight(30)
        
        form_layout.addWidget(label_residence, 3, 0)
        form_layout.addWidget(self.residence_input, 3, 1, 1, 3)
        
        # Hàng 5: Họ tên bố (*) và Họ tên mẹ (*)
        label_father = QLabel('Họ tên bố <span style="color:red; font-size:16px;">*</span>')
        label_father.setFont(QFont("Arial", 14))
        label_father.setStyleSheet("background: transparent; border: none;")
        self.father_input = QLineEdit()
        self.father_input.setPlaceholderText("Nhập họ tên bố")
        self.father_input.setFixedHeight(30)
        
        label_mother = QLabel('Họ tên mẹ <span style="color:red; font-size:16px;">*</span>')
        label_mother.setFont(QFont("Arial", 14))
        label_mother.setStyleSheet("background: transparent; border: none;")
        self.mother_input = QLineEdit()
        self.mother_input.setPlaceholderText("Nhập họ tên mẹ")
        self.mother_input.setFixedHeight(30)
        
        form_layout.addWidget(label_father, 4, 0)
        form_layout.addWidget(self.father_input, 4, 1)
        form_layout.addWidget(label_mother, 4, 2)
        form_layout.addWidget(self.mother_input, 4, 3)
        
        # Hàng 6: Số điện thoại (không bắt buộc) và Số điện thoại phụ huynh (không bắt buộc)
        label_phone = QLabel("Số điện thoại")
        label_phone.setFont(QFont("Arial", 14))
        label_phone.setStyleSheet("background: transparent; border: none;")
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Nhập số điện thoại")
        self.phone_input.setFixedHeight(30)
        
        label_parent_phone = QLabel("Số điện thoại phụ huynh")
        label_parent_phone.setFont(QFont("Arial", 14))
        label_parent_phone.setStyleSheet("background: transparent; border: none;")
        self.parent_phone_input = QLineEdit()
        self.parent_phone_input.setPlaceholderText("Nhập số điện thoại phụ huynh")
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
        self.add_button = QPushButton("Thêm học sinh")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        # Ban đầu disabled, màu xám
        self.add_button.setEnabled(False)
        self.add_button.setStyleSheet("background-color: #A9A9A9; color: white;border-radius: 8px")
        bottom_layout.addWidget(self.add_button)
        main_layout.addLayout(bottom_layout)
        
        # Kết nối sự kiện: kiểm tra các ô bắt buộc để bật/tắt nút
        self.name_input.textChanged.connect(self.check_input)
        self.hometown_input.textChanged.connect(self.check_input)
        self.residence_input.textChanged.connect(self.check_input)
        self.father_input.textChanged.connect(self.check_input)
        self.mother_input.textChanged.connect(self.check_input)
        
        # Nút Thêm được kết nối sự kiện
        self.add_button.clicked.connect(self.add_student)
    
    def check_input(self):
        # Các ô bắt buộc: Tên học sinh, Quê Quán, Tạm trú, Họ tên bố, Họ tên mẹ
        if (self.name_input.text().strip() and
            self.hometown_input.text().strip() and
            self.residence_input.text().strip() and
            self.father_input.text().strip() and
            self.mother_input.text().strip()):
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
        father = self.father_input.text().strip()
        mother = self.mother_input.text().strip()
        phone = self.phone_input.text().strip()
        parent_phone = self.parent_phone_input.text().strip()
        
        print(f"Thêm học sinh: {name}, {gender}, {dob}, {hometown}, {residence}, {father}, {mother}, {phone}, {parent_phone}")
        self.show_notification()
    
    def show_notification(self):
        # Tạo QDialog che phủ toàn bộ form
        notif = QDialog(self, flags=Qt.FramelessWindowHint)
        notif.setModal(True)
        notif.setAttribute(Qt.WA_TranslucentBackground)
        notif.resize(self.size())
        
        # Tạo khung thông báo nằm giữa form
        frame = QFrame(notif)
        frame.setStyleSheet("background-color: #28a745; border-radius: 8px;")
        frame.setFixedSize(300, 60)
        frame.move((notif.width() - frame.width()) // 2, (notif.height() - frame.height()) // 2)
        
        label = QLabel("Thêm học sinh thành công", frame)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        label.resize(frame.size())
        
        notif.show()
        QTimer.singleShot(2000, notif.accept)
    
    def go_back(self):
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(0)
