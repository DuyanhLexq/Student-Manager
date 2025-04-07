import logging
from GUI.util import formPage
from GUI.Class.addClass_func import AddClassPage
from GUI.Class.alterClass_func import AlterClassPage
from GUI.util import get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_PREVIEW_CLASSES_DATA_QUERY

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class classPage(formPage):
    """
    Class management page that extends the formPage.

    This page allows users to view, add, and edit class information.
    It connects to the main stacked widget to allow page navigation.

    Attributes:
        main_stack (QStackedWidget): Stack widget used to switch between pages.
        preview_data (list): Preview data for displaying the class table.
    """

    def __init__(self, main_stack=None):
        """
        Initializes the classPage with class data and UI elements.

        Args:
            main_stack (QStackedWidget, optional): The stack containing all pages for navigation.
        """
        self.main_stack = main_stack
        # Get preview data for the class table
        self.preview_data = get_right_table_data_form(get_preview_data(GET_PREVIEW_CLASSES_DATA_QUERY))
        
        logger.info("Class preview data loaded successfully.")

        # Initialize the base formPage with configuration
        super().__init__(
            self.preview_data,
            field=["Chọn", "ID", "Tên", "Số lượng học sinh", "Ngày tạo"],
            title="Quản lý lớp",
            main_stack=self.main_stack,
            search_text="Tìm kiếm học sinh",
            filter_fields=["ID", "Tên", "Số lượng học sinh", "Ngày tạo"]
        )

    def go_to_add_page(self):
        """
        Navigates to the AddClassPage to allow users to add a new class.
        """
        if self.main_stack:
            add_page = AddClassPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
            logger.info("Navigated to AddClassPage.")
        else:
            logger.warning("Main stack not provided. Cannot navigate to AddClassPage.")

    def go_to_edit_page(self):
        """
        Navigates to the AlterClassPage for editing the selected class.
        """
        # Get selected class ID from the table
        class_id = self.get_id_selected()
        if class_id is None:
            logger.warning("No class selected for editing.")
            return

        if self.main_stack:
            edit_page = AlterClassPage(parent_stack=self.main_stack, class_id=class_id)
            self.main_stack.addWidget(edit_page)
            self.main_stack.setCurrentWidget(edit_page)
            logger.info(f"Navigated to AlterClassPage for class ID: {class_id}.")
        else:
            logger.warning("Main stack not provided. Cannot navigate to AlterClassPage.")
