from PyQt5.QtGui import QPixmap, QPainter, QIcon,QPainterPath
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QCompleter, QDialog,QComboBox,QSpacerItem,QSizePolicy,QMessageBox,QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from typing import List,Union,Optional
from GUI.config import FILTER_ICON_PATH,REFRESH_ICON_PATH
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

def get_right_table_data_form(data: List[tuple[str]]) -> List[List[str]]:
    res = []
    for dt in data:
        accurate_data = list(map(lambda value: str(value), dt))
        res.append(accurate_data)
    return res

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
                 single_select:bool = False,
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
        self.single_select = single_select
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
        # Tạo danh sách gợi ý từ tất cả các field (trừ cột "Chọn" nếu có)
        suggestions = set()
        for row in self.sample_data:
            # Nếu có cột "Chọn", giả sử dữ liệu thực bắt đầu từ index 0 của row
            for cell in row:
                if cell.strip():
                    suggestions.add(cell)
        completer = QCompleter(sorted(list(suggestions)))
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
            # Thêm nút Refresh bên trái
            self.refresh_button = QPushButton()
            self.refresh_button.setIcon(QIcon(REFRESH_ICON_PATH))
            self.refresh_button.setIconSize(self.refresh_button.sizeHint())
            self.refresh_button.setFixedSize(30, 30)
            self.refresh_button.setCursor(Qt.PointingHandCursor)
            self.refresh_button.clicked.connect(self.refresh_table)
            filter_layout.addWidget(self.refresh_button)
            
            # Spacer để đẩy các thành phần về phía bên phải
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
                    item = QTableWidgetItem(data_row[data_index])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # không Editable
                    self.table.setItem(row, col, item)
        main_layout.addWidget(self.table)

        # Kết nối sự kiện cho các nút
        self.add_button.clicked.connect(self.go_to_add_page)
        self.edit_button.clicked.connect(self.go_to_edit_page)
        self.delete_button.clicked.connect(self.delete)
        self.table.itemChanged.connect(self.handle_single_selection)

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
        if hasattr(self, 'refresh_button'):
            self.refresh_button.setStyleSheet(button_style)
        if hasattr(self, 'filter_button'):
            self.filter_button.setStyleSheet(button_style)
    
    def handle_single_selection(self, item):
        if not self.single_select or item.column() != 0:
            return

        # Nếu checkbox được check
        if item.checkState() == Qt.Checked:
            modifiers = QApplication.keyboardModifiers()
            allow_multi = modifiers & (Qt.ShiftModifier | Qt.ControlModifier)

            if not allow_multi:
                # Bỏ chọn tất cả dòng khác
                for row in range(self.table.rowCount()):
                    current_item = self.table.item(row, 0)
                    if current_item is not item:
                        current_item.setCheckState(Qt.Unchecked)


    def search_student(self):
        query = self.search_input.text().strip().lower()
        print(f"{self.search_text}: {query}")
        # Tìm kiếm theo tất cả các field (bỏ qua cột "Chọn" ở cột 0)
        for row in range(self.table.rowCount()):
            match = False
            # Duyệt qua các cột từ cột 1 trở đi
            for col in range(1, self.table.columnCount()):
                item = self.table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            if match:
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

    def refresh_table(self):
        """Làm mới bảng: xóa nội dung tìm kiếm và hiển thị lại tất cả các dòng."""
        self.search_input.clear()
        for row in range(self.table.rowCount()):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, checkbox_item)
            self.table.showRow(row)
        print("Bảng đã được làm mới.")

    def go_to_add_page(self):
        if self.main_stack:
            print("Chuyển sang trang thêm mới")
            # Ví dụ: Giả sử add_page là một lớp khác, cần khởi tạo và chuyển trang:
            # add_page_instance = add_page(parent_stack=self.main_stack)
            # self.main_stack.addWidget(add_page_instance)
            # self.main_stack.setCurrentWidget(add_page_instance)
        else:
            print("Main stack chưa được cung cấp!")
    
    def get_id_selected(self) -> Optional[str]:
        # Lấy danh sách các dòng được chọn qua checkbox
        selected_rows = []
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                selected_rows.append(row)
        
        # Kiểm tra: chỉ cho phép sửa khi chọn đúng 1 giáo viên
        if len(selected_rows) != 1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn đúng 1 đối tượng để sửa thông tin!")
            return

        selected_row = selected_rows[0]
        # Giả sử cột 1 chứa ID của giáo viên
        id_item = self.table.item(selected_row, 1)
        if id_item is None:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy thông tin ID!")
            return

        _id = id_item.text()
        print(f"Sửa thông tin có ID: {_id}")
        return _id


    def go_to_edit_page(self):
        print("Sửa thông tin học sinh")

    def delete(self):
        """Xóa các dòng được chọn trong bảng.
        Nếu không có dòng nào được chọn, hiển thị thông báo.
        Nếu có nhiều dòng được chọn, hiển thị thông báo xác nhận với danh sách các học sinh được chọn.
        Nếu chỉ có một dòng được chọn, hiển thị thông báo xác nhận với thông tin của học sinh đó.
        """
        selected = []
        # Duyệt qua các dòng của bảng để lấy những dòng có checkbox được tích
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                # Lấy thông tin ID (cột 1) và Tên (cột 2)
                _id = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
                selected.append((row,_id))
        
        if not selected:
            QMessageBox.information(self, "Thông báo", "Chưa chọn phần tử nào để xóa.")
            return
        
        # Tạo thông báo xác nhận dựa trên số lượng học sinh được chọn
        if len(selected) == 1:
            _id= selected[0][1]
            confirmation_message = f"Xác nhận xóa phần tử có ID là {_id}?"
        else:
            details = "\n".join([f"ID-{_id}" for (_,_id) in selected])
            confirmation_message = f"Xác nhận xóa các phần tử có ID:\n{details}"
        
        reply = QMessageBox.question(
            self, 
            "Xác nhận xóa", 
            confirmation_message,
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Xóa các dòng từ dưới lên để tránh làm lệch thứ tự
            for row,_ in reversed(selected):
                self.table.removeRow(row)
            print("Đã xóa các mục đã chọn.")
        else:
            print("Hủy xóa.")