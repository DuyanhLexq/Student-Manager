import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView, QCompleter, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from GUI.config import FILTER_ICON_PATH, REFRESH_ICON_PATH

# Setup logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Custom QLineEdit to emit returnPressed when Enter is pressed
class CustomLineEdit(QLineEdit):
    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.returnPressed.emit()
            event.accept()
        else:
            super().keyPressEvent(event)

class TableSelectorWidget(QWidget):
    """
    A custom widget that provides a searchable, filterable, and optionally selectable table.

    Attributes:
        sample_data (list): 2D list of data to display.
        field (list): List of column names. If the first is "Chọn", it enables checkboxes.
        title (str): Title displayed above the table.
        search_text (str): Placeholder text for the search input.
        filter_fields (list): List of field names available for sorting/filtering.
        single_selection (bool): If True, only one checkbox can be selected at a time.
    """

    def __init__(self, data, field, title="", search_text="Tìm kiếm", filter_fields=[], parent=None, single_selection=False):
        super().__init__(parent)
        self.sample_data = data
        self.field = field
        self.title = title
        self.search_text = search_text
        self.filter_fields = filter_fields
        self.single_selection = single_selection

        logger.info("Initializing TableSelectorWidget")
        self.initUI()
        self.applyStyles()

    def initUI(self):
        """
        Initializes the UI layout, including title, search box, filter controls, and table.
        """
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Title label
        if self.title:
            title_label = QLabel(self.title)
            title_label.setFont(QFont("Arial", 16, QFont.Bold))
            title_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(title_label)

        # Search bar with suggestions
        search_layout = QHBoxLayout()
        self.search_input = CustomLineEdit()
        self.search_input.setPlaceholderText(self.search_text)
        self.search_input.setFixedHeight(30)

        # Autocomplete suggestions
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

        # Filter controls
        if self.filter_fields:
            filter_layout = QHBoxLayout()

            # Refresh button
            self.refresh_button = QPushButton()
            self.refresh_button.setIcon(QIcon(REFRESH_ICON_PATH))
            self.refresh_button.setFixedSize(30, 30)
            self.refresh_button.setCursor(Qt.PointingHandCursor)
            self.refresh_button.clicked.connect(self.refresh_table)
            filter_layout.addWidget(self.refresh_button)

            # Spacer
            spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            filter_layout.addItem(spacer)

            # ComboBox to choose filter criteria
            self.filter_combo = QComboBox()
            self.filter_combo.addItems(self.filter_fields)
            self.filter_combo.setMinimumWidth(150)
            self.filter_combo.setFixedHeight(30)
            filter_layout.addWidget(self.filter_combo)

            # Filter button
            self.filter_button = QPushButton()
            self.filter_button.setIcon(QIcon(FILTER_ICON_PATH))
            self.filter_button.setFixedSize(30, 30)
            self.filter_button.setCursor(Qt.PointingHandCursor)
            self.filter_button.clicked.connect(self.filter_data)
            filter_layout.addWidget(self.filter_button)

            main_layout.addLayout(filter_layout)

        # Table setup
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

        # Fill table with data and add checkbox to first column
        for row, data_row in enumerate(self.sample_data):
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.table.setItem(row, 0, checkbox_item)

            for col in range(1, num_cols):
                data_index = col - 1
                if data_index < len(data_row):
                    item = QTableWidgetItem(data_row[data_index])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.table.setItem(row, col, item)

        main_layout.addWidget(self.table)

        # Only allow one checkbox checked if single_selection is enabled
        if self.single_selection:
            self.table.itemChanged.connect(self.handle_checkbox_change)

    def handle_selection_changed(self, selected, deselected):
        """
        Handles row selection when Ctrl/Shift is held, syncing with checkbox states.
        """
        modifiers = QApplication.keyboardModifiers()
        if modifiers in (Qt.ControlModifier, Qt.ShiftModifier):
            for index in self.table.selectionModel().selectedRows():
                checkbox_item = self.table.item(index.row(), 0)
                if checkbox_item and checkbox_item.checkState() != Qt.Checked:
                    checkbox_item.setCheckState(Qt.Checked)

    def applyStyles(self):
        """
        Apply consistent styling to filter/refresh buttons.
        """
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
        """
        Filters rows based on the text entered in the search input.
        """
        query = self.search_input.text().strip().lower()
        for row in range(self.table.rowCount()):
            match = False
            for col in range(1, self.table.columnCount()):
                item = self.table.item(row, col)
                if item and query in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)

        logger.info(f"Search applied: '{query}'")

    def filter_data(self):
        """
        Sorts the table by the currently selected filter field in ascending order.
        """
        selected_field = self.filter_combo.currentText()
        try:
            col_index = (["Chọn"] + self.field).index(selected_field)
            self.table.sortItems(col_index, Qt.AscendingOrder)
            logger.info(f"Table sorted by field: {selected_field}")
        except ValueError:
            logger.warning(f"Invalid filter field selected: {selected_field}")

    def refresh_table(self):
        """
        Resets the table view and clears any applied search filter.
        """
        self.search_input.clear()
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, False)
        logger.info("Table refreshed.")

    def get_checked_rows(self):
        """
        Returns a list of selected rows based on checked checkboxes.

        Returns:
            list: List of row data (excluding checkbox column) that were selected.
        """
        selected_data = []
        for row in range(self.table.rowCount()):
            checkbox = self.table.item(row, 0)
            if checkbox.checkState() == Qt.Checked:
                row_data = []
                for col in range(1, self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                selected_data.append(row_data)
        logger.info(f"{len(selected_data)} row(s) selected.")
        return selected_data

    def handle_checkbox_change(self, item):
        """
        Ensures only one checkbox is selected at a time if single_selection is True.
        """
        if item.column() != 0:
            return
        if item.checkState() == Qt.Checked:
            for row in range(self.table.rowCount()):
                other_item = self.table.item(row, 0)
                if other_item is not item:
                    other_item.setCheckState(Qt.Unchecked)
            logger.info("Single checkbox enforced.")
