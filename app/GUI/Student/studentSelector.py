from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from GUI.tableSelector import TableSelectorWidget
from PyQt5.QtCore import Qt
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_PREVIEW_STUDENT_DATA_QUERY
from typing import List

class StudentSelectorDialog(QDialog):
    def __init__(self, parent=None,students_id:List[str] = []):
        super().__init__(parent)
        self.setWindowTitle("Chọn Học sinh")
        self.resize(500, 400)
        data = get_right_table_data_form(get_preview_data(GET_PREVIEW_STUDENT_DATA_QUERY))
        self.students_id = students_id
        # Sample data cho học sinh; sau này lấy từ SQL
        fields = ["Chọn", "ID", "Tên học sinh", "Giới tính", "Ngày sinh"]
        self.selector = TableSelectorWidget(data, fields, title="Chọn Học sinh", search_text="Tìm kiếm học sinh",filter_fields= ["ID", "Tên học sinh", "Giới tính", "Ngày sinh"])
        layout = QVBoxLayout(self)
        layout.addWidget(self.selector)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        ok_button = buttons.button(QDialogButtonBox.Ok)
        cancel_button = buttons.button(QDialogButtonBox.Cancel)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """)
        layout.addWidget(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.fill_checkboxes()  # Đánh dấu các checkbox đã chọn dựa trên students_id
    
    def fill_checkboxes(self):
        # Lặp qua tất cả các hàng trong bảng và kiểm tra xem ID có trong danh sách đã chọn không
        for row in range(self.selector.table.rowCount()):
            item = self.selector.table.item(row, 1)
            if item.text() in self.students_id:
                checkbox_item = self.selector.table.item(row, 0)
                if checkbox_item:
                    checkbox_item.setCheckState(Qt.Checked)

    def get_selection(self):
        return self.selector.get_checked_rows()