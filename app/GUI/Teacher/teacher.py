# -*- coding: utf-8 -*-
import logging
from GUI.Teacher.addTeacher_func import AddTeacherPage
from GUI.Teacher.alterTeacher_func import AlterTeacherPage
from GUI.Teacher.addSalary_func import AddSalaryPage
from GUI.Teacher.alterSalary_func import AlterSalaryPage
from GUI.util import formPage, get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_PREVIEW_SALARY_DATA_QUERY, GET_PREVIEW_TEACHER_DATA_QUERY


# Configure module-level logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeacherPage(formPage):
    """
    Teacher management page that displays teacher data and provides navigation for adding and editing teacher records.
    """

    def __init__(self, main_stack=None):
        """
        Initializes the TeacherPage.

        Args:
            main_stack: The main widget stack for page navigation.
        """
        self.main_stack = main_stack

        # Retrieve and process teacher preview data.
        try:
            teacher_data_raw = get_preview_data(GET_PREVIEW_TEACHER_DATA_QUERY)
            self.preview_data = get_right_table_data_form(teacher_data_raw)
            logger.info("Teacher preview data loaded successfully.")
        except Exception as e:
            logger.error("Error retrieving teacher preview data: %s", e)
            self.preview_data = []  # Use an empty list if data retrieval fails

        # Initialize the base formPage with teacher-related settings (fields and text remain in Vietnamese).
        super().__init__(
            data=self.preview_data,
            field=["Chọn", "ID", "Tên giáo viên", "Ngày sinh", "Năm vào làm việc"],
            title="Quản lý giáo viên",
            main_stack=self.main_stack,
            search_text="Tìm kiếm giáo viên",
            filter_fields=["Tên giáo viên", "Năm vào làm việc", "ID"],
            single_select=True
        )

    def go_to_add_page(self):
        """
        Navigates to the Add Teacher Page.
        """
        if not self.main_stack:
            logger.error("Main stack is not provided!")
            return
        try:
            add_page = AddTeacherPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
            logger.info("Navigated to Add Teacher Page successfully.")
        except Exception as e:
            logger.error("Error navigating to Add Teacher Page: %s", e)

    def go_to_edit_page(self):
        """
        Navigates to the Edit Teacher Page for the selected teacher.
        """
        teacher_id = self.get_id_selected()
        # The check for teacher_id is assumed to be handled by self.get_id_selected()
        if teacher_id is None:
            logger.error("No teacher ID selected for editing.")
            return
        # Check if main_stack is provided
        if not self.main_stack:
            logger.error("Main stack is not provided!")
            return

        try:
            edit_page = AlterTeacherPage(parent_stack=self.main_stack, teacher_id=teacher_id)
            self.main_stack.addWidget(edit_page)
            self.main_stack.setCurrentWidget(edit_page)
            logger.info("Navigated to Edit Teacher Page for teacher ID: %s", teacher_id)
        except Exception as e:
            logger.error("Error navigating to Edit Teacher Page: %s", e)


class SalaryPage(formPage):
    """
    Salary management page that displays teacher salary data and provides navigation for adding and editing salary details.
    """

    def __init__(self, main_stack=None):
        """
        Initializes the SalaryPage.

        Args:
            main_stack: The main widget stack for page navigation.
        """
        self.main_stack = main_stack

        # Retrieve and process salary preview data.
        try:
            salary_data_raw = get_preview_data(GET_PREVIEW_SALARY_DATA_QUERY)
            self.preview_data = get_right_table_data_form(salary_data_raw)
            logger.info("Salary preview data loaded successfully.")
        except Exception as e:
            logger.error("Error retrieving salary preview data: %s", e)
            self.preview_data = []  # Use an empty list if data retrieval fails

        # Initialize the base formPage with salary-related settings (fields and text remain in Vietnamese).
        super().__init__(
            data=self.preview_data,
            field=["Chọn", "ID", "Tên giáo viên", "Lương", "Lương thưởng"],
            title="Quản lý lương giáo viên",
            main_stack=self.main_stack,
            search_text="Tìm kiếm giáo viên",
            filter_fields=["ID", "Tên giáo viên", "Lương", "Lương thưởng"],
            single_select=True
        )

    def go_to_add_page(self):
        """
        Navigates to the Add Salary Page.
        """
        if not self.main_stack:
            logger.error("Main stack is not provided!")
            return
        try:
            add_page = AddSalaryPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
            logger.info("Navigated to Add Salary Page successfully.")
        except Exception as e:
            logger.error("Error navigating to Add Salary Page: %s", e)

    def go_to_edit_page(self):
        """
        Navigates to the Edit Salary Page for the selected teacher's salary record.
        """
        teacher_id = self.get_id_selected()
        if teacher_id is None:
            logger.error("No teacher ID selected for editing salary.")
            return
        
        if not self.main_stack:
            logger.error("Main stack is not provided!")
            return

        try:
            edit_page = AlterSalaryPage(parent_stack=self.main_stack, teacher_id=teacher_id)
            self.main_stack.addWidget(edit_page)
            self.main_stack.setCurrentWidget(edit_page)
            logger.info("Navigated to Edit Salary Page for teacher ID: %s", teacher_id)
        except Exception as e:
            logger.error("Error navigating to Edit Salary Page: %s", e)