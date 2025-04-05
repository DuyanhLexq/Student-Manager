from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from GUI.tableSelector import TableSelectorWidget
from PyQt5.QtCore import Qt

class StudentSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chọn Học sinh")
        self.resize(500, 400)
        # Sample data cho học sinh; sau này lấy từ SQL
        data = [
            ["HS001", "Học sinh A", "Nam", "15/03/2005"],
            ["HS002", "Học sinh B", "Nữ", "20/07/2006"],
            ["HS003", "Học sinh C", "Nam", "05/12/2005"],
            ["HS004", "Học sinh D", "Nữ", "25/09/2004"]
        ]
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

    def get_selection(self):
        return self.selector.get_checked_rows()