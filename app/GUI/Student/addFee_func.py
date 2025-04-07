from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QDialog, QDialogButtonBox, QListWidgetItem, QFrame,QGridLayout,QComboBox
)
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import Qt, QTimer,QSize
from GUI.config import BACK_ICON_PATH,STUDENT_FEE_PAGE_ID
from GUI.notification import FloatingNotification

class AddFeePage(QWidget):
    def __init__(self, parent_stack=None):
        super().__init__()
        self.parent_stack = parent_stack
        self.selected_grade = None
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
        
   
        label_student_name = QLabel('Tên học sinh <span style="color:red; font-size:16px;">*</span>')
        label_student_name.setFont(QFont("Arial", 14))
        label_student_name.setStyleSheet("background: transparent; border: none;")
        self.student_name_input = QLineEdit()
        self.student_name_input.setPlaceholderText("Nhập tên học sinh")
        self.student_name_input.setFixedHeight(30)
        form_layout.addWidget(label_student_name, 0, 0)
        form_layout.addWidget(self.student_name_input, 0, 1)
        
        label_fee = QLabel('Học phí <span style="color:red; font-size:16px;">*</span>')
        label_fee.setFont(QFont("Arial", 14))
        label_fee.setStyleSheet("background: transparent; border: none;")
        self.fee_line = QLineEdit()
        self.fee_line.setPlaceholderText("Nhập điểm")
        self.fee_line.setFixedHeight(30)
        fee_layout = QHBoxLayout()
        fee_layout.addWidget(self.fee_line)
        form_layout.addWidget(label_fee, 3, 0)
        form_layout.addLayout(fee_layout, 3, 1)

       
        label_paid = QLabel('Đóng <span style="color:red; font-size:16px;">*</span>')
        label_paid.setFont(QFont("Arial", 14))
        label_paid.setStyleSheet("background: transparent; border: none;")
        self.paid_combo = QComboBox()
        self.paid_combo.addItems(["Đã đóng", "Chưa đóng"])
        self.paid_combo.setCurrentText("Chưa dóng")
        self.paid_combo.setFixedHeight(30)
        self.paid_combo.setStyleSheet("QComboBox { background-color: white; }")
        paid_layout = QHBoxLayout()
        paid_layout.addWidget(self.paid_combo)
        form_layout.addWidget(label_paid, 4, 0)
        form_layout.addLayout(paid_layout, 4, 1)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        
        
        self.add_button = QPushButton("Thêm học phí")
        self.add_button.setFixedSize(150, 40)
        self.add_button.setFont(QFont("Arial", 14))
        self.add_button.setEnabled(False)
        self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border-radius: 8px;")
        self.add_button.clicked.connect(self.add_fee)
        main_layout.addWidget(self.add_button, alignment=Qt.AlignRight)
        
        # Kiểm tra điều kiện: tên lớp và giáo viên phải được nhập/chọn
        self.student_name_input.textChanged.connect(self.check_input)
        self.fee_line.textChanged.connect(self.check_input)
        self.paid_combo.currentTextChanged.connect(self.check_input)
        # Kết nối sự kiện cho các ô nhập liệu
        
    
    def check_input(self):
        if self.student_name_input.text().strip() and self.fee_line.text().strip() and self.paid_combo.currentText():
            # Các ô bắt buộc: Tên học sinh, Học phí, Đã đóng
            self.add_button.setEnabled(True)
            self.add_button.setStyleSheet("background-color: #007BFF; color: white; border: none; border-radius: 8px;")
        else:
            self.add_button.setEnabled(False)
            self.add_button.setStyleSheet("background-color: #A9A9A9; color: white; border: none; border-radius: 8px;")

    
    def add_fee(self):
        student_name = self.student_name_input.text().strip()
        fee = self.fee_line.text().strip()
        paid = self.paid_combo.currentText()
        # Kiểm tra điều kiện: tên lớp và giáo viên phải được nhập/chọn
        if not student_name or not fee or not paid:
            # Nếu không đủ thông tin, hiển thị thông báo
            print("Vui lòng nhập đầy đủ thông tin.")
            return
        print(f"Thêm Học phí: {student_name}, Học phí: {fee}, Đã đóng: {paid}")
        # Gọi hàm thêm học phí vào cơ sở dữ liệu ở đây
        self.show_notification()
    
    
    def show_notification(self):
        notif = FloatingNotification(
            "Thêm học phí thành công!",
            parent=self.parent_stack,
            bg_color="#28a745",  # Màu xanh lá
            icon_path=r"C:\Project_Python\applications\Student-Manager\app\assets\ok.png",
        )
        notif.show_bottom_center()
    
    def go_back(self):
        if self.parent_stack:
            self.parent_stack.setCurrentIndex(STUDENT_FEE_PAGE_ID)
        else:
            print("Parent stack chưa được cung cấp.")
