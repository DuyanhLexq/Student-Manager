# -*- coding: utf-8 -*-
import logging
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from GUI.tableSelector import TableSelectorWidget
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_PREVIEW_TEACHER_DATA_QUERY

# Configure module-level logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeacherSelectorDialog(QDialog):
    """
    Dialog for selecting a teacher from a table.

    Attributes:
        teacher_id (str): The ID of the teacher to be pre-selected in the table.
    """

    def __init__(self, parent=None, teacher_id: str = None):
        """
        Initializes the TeacherSelectorDialog.

        Args:
            parent: The parent widget.
            teacher_id (str): The teacher ID to pre-select (if any).
        """
        super().__init__(parent)
        self.setWindowTitle("Chọn Giáo viên")
        self.resize(500, 400)

        # Retrieve and process teacher preview data.
        try:
            data_raw = get_preview_data(GET_PREVIEW_TEACHER_DATA_QUERY)
            data = get_right_table_data_form(data_raw)
            logger.info("Teacher preview data loaded successfully.")
        except Exception as e:
            logger.error("Error retrieving teacher preview data: %s", e)
            data = []  # Fallback to an empty list in case of error

        self.teacher_id = teacher_id
        fields = ["Chọn", "ID", "Tên giáo viên", "Ngày sinh", "Năm vào làm việc"]

        # Initialize the table selector widget with the data.
        self.selector = TableSelectorWidget(
            data, 
            fields, 
            title="Chọn Giáo viên", 
            search_text="Tìm kiếm giáo viên",
            filter_fields=["ID", "Tên giáo viên", "Ngày sinh", "Năm vào làm việc"]
        )

        # Set up the layout for the dialog.
        layout = QVBoxLayout(self)
        layout.addWidget(self.selector)

        # Create dialog buttons (OK and Cancel) with CSS styling.
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

        # Connect table item changes to ensure only one selection is active.
        self.selector.table.itemChanged.connect(self.ensureSingleSelection)
        self.fill_checkboxes()  # Pre-select checkbox based on teacher_id

    def fill_checkboxes(self):
        """
        Pre-selects the checkbox in the table if the teacher ID matches the provided teacher_id.
        """
        if self.teacher_id is None:
            logger.info("No teacher_id provided for pre-selection.")
            return

        for row in range(self.selector.table.rowCount()):
            id_item = self.selector.table.item(row, 1)
            if id_item and id_item.text() == self.teacher_id:
                checkbox_item = self.selector.table.item(row, 0)
                if checkbox_item:
                    checkbox_item.setCheckState(Qt.Checked)
                    logger.info("Pre-selected teacher ID %s at row %d.", self.teacher_id, row)
                    break
        else:
            logger.warning("Teacher ID %s not found in the table.", self.teacher_id)

    def ensureSingleSelection(self, changed_item):
        """
        Ensures that only one checkbox remains selected in the table. When a checkbox in column 0 is checked,
        all other checkboxes are unchecked.

        Args:
            changed_item: The table item that has changed.
        """
        if changed_item.column() == 0 and changed_item.checkState() == Qt.Checked:
            row_to_keep = changed_item.row()
            logger.info("Checkbox at row %d selected; ensuring single selection.", row_to_keep)
            # Block signals to prevent recursion
            self.selector.table.blockSignals(True)
            for row in range(self.selector.table.rowCount()):
                if row != row_to_keep:
                    item = self.selector.table.item(row, 0)
                    if item and item.checkState() == Qt.Checked:
                        item.setCheckState(Qt.Unchecked)
                        logger.debug("Unchecked checkbox at row %d.", row)
            self.selector.table.blockSignals(False)

    def get_selection(self):
        """
        Returns the first selected row from the table, if any.

        Returns:
            The first selected row data or None if no selection exists.
        """
        selected = self.selector.get_checked_rows()
        if selected:
            logger.info("Teacher selection retrieved from the dialog.")
            return selected[0]  # Only the first row is returned (only one selection is allowed)
        logger.info("No teacher selected in the dialog.")
        return None