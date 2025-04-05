from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from GUI.tableSelector import TableSelectorWidget
from PyQt5.QtCore import Qt

class TeacherSelectorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chọn Giáo viên")
        self.resize(500, 400)
        # Sample data cho giáo viên; sau này dữ liệu sẽ được lấy từ SQL
        data = [
            ["GV001", "Nguyễn Văn A", "01/01/1980", "2010"],
            ["GV002", "Trần Thị B", "05/03/1985", "2012"],
            ["GV003", "Lê Văn C", "12/07/1978", "2008"]
        ]
        fields = ["Chọn", "ID", "Tên giáo viên", "Ngày sinh", "Năm vào làm việc"]
        self.selector = TableSelectorWidget(data, fields, title="Chọn Giáo viên", search_text="Tìm kiếm giáo viên",filter_fields= ["ID", "Tên giáo viên", "Ngày sinh", "Năm vào làm việc"])
        layout = QVBoxLayout(self)
        layout.addWidget(self.selector)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # Áp dụng CSS cho nút OK và Cancel
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

        # Đảm bảo chỉ cho phép chọn 1 dòng: khi một checkbox được bật, tắt các dòng khác
        self.selector.table.itemChanged.connect(self.ensureSingleSelection)

    def ensureSingleSelection(self, changed_item):
        # Nếu checkbox (cột 0) được chỉnh sửa và được bật, tắt các checkbox khác
        if changed_item.column() == 0 and changed_item.checkState() == Qt.Checked:
            row_to_keep = changed_item.row()
            # Tạm dừng signal để tránh gọi đệ quy
            self.selector.table.blockSignals(True)
            for row in range(self.selector.table.rowCount()):
                if row != row_to_keep:
                    item = self.selector.table.item(row, 0)
                    if item.checkState() == Qt.Checked:
                        item.setCheckState(Qt.Unchecked)
            self.selector.table.blockSignals(False)

    def get_selection(self):
        selected = self.selector.get_checked_rows()
        if selected:
            return selected[0]  # chỉ lấy dòng đầu nếu có nhiều (chỉ cho phép chọn 1)
        return None
