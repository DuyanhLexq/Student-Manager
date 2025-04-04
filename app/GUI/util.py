from PyQt5.QtGui import QPixmap, QPainter, QIcon,QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter, QDialog,QComboBox,QSpacerItem,QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from typing import List
from GUI.config import FILTER_ICON_PATH
import datetime





def convert_icon_to_white(icon_path:str) -> QPixmap:
    # Tạo một QPixmap mới với cùng kích thước, nền trong suốt
    pixmap = QPixmap(icon_path)
    
    white_pixmap = QPixmap(pixmap.size())
    white_pixmap.fill(Qt.transparent)

    # Dùng QPainter để vẽ icon cũ lên white_pixmap và chuyển màu
    painter = QPainter(white_pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
    painter.fillRect(white_pixmap.rect(), Qt.white)
    painter.end()
    return white_pixmap

def get_rounded_pixmap(pixmap, diameter):
    # Tạo một QPixmap mới với kích thước và nền trong suốt
    rounded = QPixmap(diameter, diameter)
    rounded.fill(Qt.transparent)
    
    # Chuyển đổi ảnh đã scale thành kích thước mong muốn nếu chưa đạt kích thước này
    pixmap = pixmap.scaled(diameter, diameter, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    
    # Sử dụng QPainter để vẽ hình tròn và cắt ảnh
    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addEllipse(0, 0, diameter, diameter)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    return rounded



class formPage(QWidget):
    def __init__(self,
                 data,
                 field: List[str],
                 title: str,
                 main_stack=None,
                 **args):
        """
        :param data: Dữ liệu mẫu của bảng, mỗi phần tử là một danh sách các giá trị cho các field.
        :param field: Danh sách tên các field. Nếu field[0] là "Chọn", thì cột đầu tiên sẽ dành cho checkbox.
        :param title: Tiêu đề của trang (ví dụ: "Quản lý điểm").
        :param main_stack: QStackedWidget chứa các trang của ứng dụng, dùng để chuyển trang.
        :param args: Các tham số khác, ví dụ:
                     - search_text: hiển thị placeholder cho ô tìm kiếm.
                     - filter_fields: danh sách tiêu chí filter (ví dụ: ["Tuổi", "ID", "Tên"]).
        """
        super().__init__()
        self.sample_data = data
        self.main_stack = main_stack
        self.field = field
        self.title = title
        self.search_text = args.get("search_text", "Tìm kiếm")
        self.filter_fields = args.get("filter_fields", [])
        self.initUI()
        self.applyStyles()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Tiêu đề trang
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Layout tìm kiếm (ở phía trên)
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(f"{self.search_text}...")
        self.search_input.setFixedHeight(30)
        # Giả sử dữ liệu tìm kiếm ở cột đầu tiên của sample_data (có thể điều chỉnh lại)
        name_list = [row[0] if len(row) > 0 else "" for row in self.sample_data]
        completer = QCompleter(name_list)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_input.setCompleter(completer)
        self.search_input.returnPressed.connect(self.search_student)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Nút chức năng: Thêm, Sửa, Xóa, Biểu đồ
        func_button_layout = QHBoxLayout()
        self.add_button = QPushButton("Thêm")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        self.chart_button = QPushButton("Biểu đồ")
        for btn in [self.add_button, self.edit_button, self.delete_button, self.chart_button]:
            btn.setFixedHeight(30)
            btn.setFont(QFont("Arial", 12))
            btn.setCursor(Qt.PointingHandCursor)
            func_button_layout.addWidget(btn)
        main_layout.addLayout(func_button_layout)

        # Khu vực Filter (đặt bên phải, ngay dưới các nút chức năng)
        if self.filter_fields:
            filter_layout = QHBoxLayout()
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            filter_layout.addItem(spacer)
            # ComboBox filter với kích thước tối thiểu
            self.filter_combo = QComboBox()
            self.filter_combo.addItems(self.filter_fields)
            self.filter_combo.setMinimumWidth(150)
            self.filter_combo.setMinimumHeight(30)
           
            # Nút Filter là hình ảnh "filter.png"
            self.filter_button = QPushButton()
            self.filter_button.setIcon(QIcon(FILTER_ICON_PATH))
            self.filter_button.setIconSize(self.filter_button.sizeHint())
            # Đặt kích thước cố định cho nút (ví dụ 30x30)
            self.filter_button.setFixedSize(30, 30)
            self.filter_button.setCursor(Qt.PointingHandCursor)
            self.filter_button.clicked.connect(self.filter_table)
            filter_layout.addWidget(self.filter_combo)
            filter_layout.addWidget(self.filter_button)
            main_layout.addLayout(filter_layout)

        # Xác định số cột và header dựa trên field
        if self.field and self.field[0].strip().lower() == "chọn":
            num_cols = len(self.field)
            headers = self.field
        else:
            num_cols = 1 + len(self.field)
            headers = ["Chọn"] + self.field

        self.table = QTableWidget()
        self.table.setColumnCount(num_cols)
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setRowCount(len(self.sample_data))

        for row, data_row in enumerate(self.sample_data):
            # Thêm checkbox vào cột đầu tiên
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, checkbox_item)
            # Gán dữ liệu cho các cột còn lại
            for col in range(1, num_cols):
                data_index = col - 1  # data_row[0] -> bảng cột 1, data_row[1] -> bảng cột 2, ...
                if data_index < len(data_row):
                    self.table.setItem(row, col, QTableWidgetItem(data_row[data_index]))
        main_layout.addWidget(self.table)

        # Kết nối sự kiện cho các nút
        self.add_button.clicked.connect(self.go_to_add_page)
        self.edit_button.clicked.connect(self.edit_student)
        self.delete_button.clicked.connect(self.delete_student)

    def applyStyles(self):
        button_style = """
        QPushButton {
            border: none;
            background-color: transparent;
            font-weight: normal;
            text-decoration: none;
        }
        QPushButton:hover {
            text-decoration: underline;
            background-color: #d3d3d3;
        }
        QPushButton:pressed {
            background-color: #d3d3d3;
        }
    """
        for btn in [self.add_button, self.edit_button, self.delete_button, self.chart_button]:
            btn.setStyleSheet(button_style)

    def search_student(self):
        query = self.search_input.text().strip()
        print(f"{self.search_text}: {query}")
        # Tìm kiếm theo cột thứ 2 (với checkbox là cột 0)
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 2)
            if item and query.lower() in item.text().lower():
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def filter_table(self):
        """Sắp xếp bảng theo tiêu chí được chọn (sắp xếp tăng dần)."""
        selected_field = self.filter_combo.currentText()
        col_index = None
        # Nếu field[0] là "Chọn", header thực tế của bảng là field nguyên bản
        if self.field and self.field[0].strip().lower() == "chọn":
            try:
                col_index = self.field.index(selected_field)
            except ValueError:
                col_index = None
        else:
            # Nếu không có "Chọn" ở field, header là ["Chọn"] + self.field
            try:
                col_index = (["Chọn"] + self.field).index(selected_field)
            except ValueError:
                col_index = None

        if col_index is None:
            print("Tiêu chí filter không hợp lệ!")
            return

        # Sắp xếp bảng theo cột đã chọn (theo thứ tự tăng dần)
        self.table.sortItems(col_index, Qt.AscendingOrder)
        print(f"Bảng đã được sắp xếp theo {selected_field} (tăng dần).")

    def go_to_add_page(self):
        if self.main_stack:
            print("Chuyển sang trang thêm mới")
            # Ví dụ: Giả sử add_page là một lớp khác, cần khởi tạo và chuyển trang:
            # add_page_instance = add_page(parent_stack=self.main_stack)
            # self.main_stack.addWidget(add_page_instance)
            # self.main_stack.setCurrentWidget(add_page_instance)
        else:
            print("Main stack chưa được cung cấp!")

    def edit_student(self):
        print("Sửa thông tin học sinh")

    def delete_student(self):
        print("Xóa học sinh")