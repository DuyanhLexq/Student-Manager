from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView, QCompleter, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from GUI.config import FILTER_ICON_PATH, REFRESH_ICON_PATH  # Giả sử bạn đã định nghĩa REFRESH_ICON_PATH

# Lớp CustomLineEdit như đã định nghĩa trước để xử lý phím Enter
class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.returnPressed.emit()
            event.accept()
        else:
            super().keyPressEvent(event)

class TableSelectorWidget(QWidget):
    def __init__(self, data, field, title="", search_text="Tìm kiếm", filter_fields=[], parent=None, single_selection=False):
        """
        :param data: Danh sách dữ liệu mẫu, mỗi phần tử là một list các giá trị.
        :param field: Danh sách tên cột; nếu field[0] là "Chọn" thì cột đầu tiên dùng cho checkbox.
        :param title: Tiêu đề hiển thị ở trên bảng (có thể rỗng).
        :param search_text: Text hiển thị trong ô tìm kiếm.
        :param filter_fields: Danh sách tiêu chí filter (ví dụ: ["Tuổi", "ID", "Tên"]).
        :param parent: Parent widget.
        :param single_selection: Nếu True, chỉ cho phép 1 checkbox được tick (chế độ single selection).
        """
        super().__init__(parent)
        self.sample_data = data
        self.field = field
        self.title = title
        self.search_text = search_text
        self.filter_fields = filter_fields
        self.single_selection = single_selection
        self.initUI()
        self.applyStyles()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Tiêu đề (nếu có)
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(QFont("Arial", 16, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(title_label)

        # Layout tìm kiếm sử dụng CustomLineEdit để xử lý phím Enter
        search_layout = QHBoxLayout()
        self.search_input = CustomLineEdit()
        self.search_input.setPlaceholderText(self.search_text)
        self.search_input.setFixedHeight(30)
        # Tạo danh sách gợi ý từ tất cả các field (trừ cột "Chọn" nếu có)
        suggestions = set()
        for row in self.sample_data:
            for cell in row:
                if cell.strip():
                    suggestions.add(cell)
        completer = QCompleter(sorted(list(suggestions)))
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.search_input.setCompleter(completer)
        self.search_input.returnPressed.connect(self.search_data)
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)

        # Layout Filter nếu có
        if self.filter_fields:
            filter_layout = QHBoxLayout()
            # Nút refresh bên trái
            self.refresh_button = QPushButton()
            self.refresh_button.setIcon(QIcon(REFRESH_ICON_PATH))
            self.refresh_button.setIconSize(self.refresh_button.sizeHint())
            self.refresh_button.setFixedSize(30, 30)
            self.refresh_button.setCursor(Qt.PointingHandCursor)
            self.refresh_button.clicked.connect(self.refresh_table)
            filter_layout.addWidget(self.refresh_button)

            # Spacer (có thể điều chỉnh vị trí nếu cần)
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            filter_layout.addItem(spacer)

            # ComboBox filter
            self.filter_combo = QComboBox()
            self.filter_combo.addItems(self.filter_fields)
            self.filter_combo.setMinimumWidth(150)
            self.filter_combo.setFixedHeight(30)
            filter_layout.addWidget(self.filter_combo)

            # Nút filter với icon filter.png
            self.filter_button = QPushButton()
            self.filter_button.setIcon(QIcon(FILTER_ICON_PATH))
            self.filter_button.setIconSize(self.filter_button.sizeHint())
            self.filter_button.setFixedSize(30, 30)
            self.filter_button.setCursor(Qt.PointingHandCursor)
            self.filter_button.clicked.connect(self.filter_data)
            filter_layout.addWidget(self.filter_button)
            main_layout.addLayout(filter_layout)

        # Tạo bảng
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
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.MultiSelection)
        self.table.selectionModel().selectionChanged.connect(self.handle_selection_changed)

        for row, data_row in enumerate(self.sample_data):
            # Thêm checkbox vào cột đầu tiên
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, checkbox_item)
            # Gán dữ liệu vào các cột còn lại và không cho phép chỉnh sửa
            for col in range(1, num_cols):
                data_index = col - 1
                if data_index < len(data_row):
                    item = QTableWidgetItem(data_row[data_index])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table.setItem(row, col, item)
        main_layout.addWidget(self.table)

        # Nếu chế độ single_selection được bật, kết nối sự kiện để chỉ cho phép 1 checkbox
        if self.single_selection:
            self.table.itemChanged.connect(self.handle_checkbox_change)

    def handle_selection_changed(self, selected, deselected):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
            for index in self.table.selectionModel().selectedRows():
                checkbox_item = self.table.item(index.row(), 0)
                if checkbox_item and checkbox_item.checkState() != Qt.Checked:
                    checkbox_item.setCheckState(Qt.Checked)

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
        if hasattr(self, 'filter_button'):
            self.filter_button.setStyleSheet(button_style)
        if hasattr(self, 'refresh_button'):
            self.refresh_button.setStyleSheet(button_style)

    def search_data(self):
        """Tìm kiếm theo tất cả các field (trừ cột 'Chọn')."""
        query = self.search_input.text().strip().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(1, self.table.columnCount()):
                item = self.table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            if match:
                self.table.showRow(row)
            else:
                self.table.hideRow(row)

    def filter_data(self):
        """Sắp xếp bảng theo tiêu chí được chọn (tăng dần)."""
        selected_field = self.filter_combo.currentText()
        col_index = None
        if self.field and self.field[0].strip().lower() == "chọn":
            try:
                col_index = self.field.index(selected_field)
            except ValueError:
                col_index = None
        else:
            try:
                col_index = (["Chọn"] + self.field).index(selected_field)
            except ValueError:
                col_index = None

        if col_index is None:
            print("Tiêu chí filter không hợp lệ!")
            return

        self.table.sortItems(col_index, Qt.AscendingOrder)
        print(f"Bảng đã được sắp xếp theo {selected_field} (tăng dần).")

    def refresh_table(self):
        """Làm mới bảng: xóa nội dung tìm kiếm và hiển thị lại tất cả các dòng."""
        self.search_input.clear()
        for row in range(self.table.rowCount()):
            self.table.showRow(row)
        print("Bảng đã được làm mới.")

    def get_checked_rows(self):
        """Lấy danh sách các dòng được chọn qua checkbox (bỏ qua cột 'Chọn')."""
        selected_data = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.item(row, 0)
            if checkbox.checkState() == Qt.Checked:
                row_data = []
                for col in range(1, self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                selected_data.append(row_data)
        return selected_data

    def handle_checkbox_change(self, item):
        # Nếu item không nằm ở cột 0, bỏ qua
        if item.column() != 0:
            return
        # Nếu trạng thái của checkbox thay đổi và đang được tick
        if item.checkState() == Qt.Checked:
            for row in range(self.table.rowCount()):
                other_item = self.table.item(row, 0)
                if other_item is not item:
                    other_item.setCheckState(Qt.Unchecked)
