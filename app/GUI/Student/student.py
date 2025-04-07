# -*- coding: utf-8 -*-
import logging
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import (
    QVBoxLayout, QDialog, QMessageBox
)

from PyQt5.QtCore import Qt

# Import Student related pages for navigation
from GUI.Student.addStudent_func import AddStudentPage  # Widget for adding student
from GUI.Student.alterStudent_func import AlterStudentPage  # Widget for editing student
from GUI.Student.addGrades_func import AddGradePage  # Widget for adding grades
from GUI.Student.alterGrades_func import AltergradesPage  # Widget for editing grades
from GUI.Student.addFee_func import AddFeePage  # Widget for adding tuition fee
from GUI.Student.alterFee_func import AlterFeePage  # Widget for editing tuition fee

# Utility and data functions
from GUI.util import formPage, get_right_table_data_form
from functions.functions import get_preview_data
from sqlQuery import GET_PREVIEW_STUDENT_DATA_QUERY, GET_GRADES_DATA_QUERY, GET_TUITION_DATA_QUERY

# Configure module-level logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def delete(self):
    """
    Override the delete method to display a confirmation dialog before deleting student records.
    
    If only one student is selected, the dialog shows: 
      "Xác nhận xóa học sinh [ID]- [Tên]?"
    If multiple students are selected, it lists the selected students.
    
    Args:
        self: The instance of the formPage class containing the student table.
    """
    selected_students = []
    # Loop through table rows to get rows with checked checkboxes
    for row in range(self.table.rowCount()):
        checkbox_item = self.table.item(row, 0)
        if checkbox_item and checkbox_item.checkState() == Qt.Checked:
            # Retrieve student ID (column 1) and Name (column 2)
            student_id = self.table.item(row, 1).text() if self.table.item(row, 1) else ""
            student_name = self.table.item(row, 2).text() if self.table.item(row, 2) else ""
            selected_students.append((row, student_id, student_name))
    
    if not selected_students:
        QMessageBox.information(self, "Thông báo", "Chưa chọn học sinh nào để xóa.")
        logger.info("No student selected for deletion.")
        return
    
    # Create confirmation message based on number of selected students
    if len(selected_students) == 1:
        _, student_id, student_name = selected_students[0]
        confirmation_message = f"Xác nhận xóa học sinh {student_id}- {student_name}?"
    else:
        details = "\n".join([f"{stud_id}- {stud_name}" for (_, stud_id, stud_name) in selected_students])
        confirmation_message = f"Xác nhận xóa các học sinh:\n{details}"
    
    reply = QMessageBox.question(
        self, 
        "Xác nhận xóa", 
        confirmation_message,
        QMessageBox.Yes | QMessageBox.No, 
        QMessageBox.No
    )
    
    if reply == QMessageBox.Yes:
        # Remove rows in reverse order to avoid shifting row indexes
        for row, _, _ in reversed(selected_students):
            self.table.removeRow(row)
        logger.info("Deleted selected student(s): %s", selected_students)
        print("Đã xóa các mục đã chọn.")
    else:
        logger.info("Student deletion cancelled.")
        print("Hủy xóa.")


class ChartWindow(QDialog):
    """
    Dialog window to display statistical charts based on student data.
    
    This window creates two charts:
        - A bar chart showing the number of male/female students.
        - A histogram displaying the age distribution of students.
    """
    def __init__(self, student_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Biểu đồ thống kê")
        self.resize(800, 600)
        self.student_data = student_data
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # Create matplotlib figure and two subplots for gender and age
        self.figure, (self.ax_gender, self.ax_age) = plt.subplots(1, 2, figsize=(10, 4))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.plot_charts()

    def plot_charts(self):
        """
        Processes student data to plot:
            - A bar chart for gender count.
            - A histogram for age distribution.
        """
        genders = {"Nam": 0, "Nữ": 0}
        ages = []
        current_year = datetime.datetime.now().year

        for data in self.student_data:
            # Expect gender at index 2 and date of birth at index 3 (format: dd/mm/yyyy)
            gender = data[2].strip()
            dob_str = data[3].strip()
            try:
                day, month, year = map(int, dob_str.split("/"))
                age = current_year - year
                ages.append(age)
            except Exception as e:
                logger.error("Error converting date of birth '%s': %s", dob_str, e)
                continue

            if gender in genders:
                genders[gender] += 1

        # Plot gender bar chart
        self.ax_gender.clear()
        self.ax_gender.bar(genders.keys(), genders.values(), color=['#3498db', '#e74c3c'])
        self.ax_gender.set_title("Số lượng Nam/Nữ")
        self.ax_gender.set_ylabel("Số lượng")

        # Plot age histogram
        self.ax_age.clear()
        if ages:
            self.ax_age.hist(ages, bins=range(min(ages), max(ages) + 2), color='#2ecc71', edgecolor='black')
            self.ax_age.set_title("Phân bố độ tuổi")
            self.ax_age.set_xlabel("Độ tuổi")
            self.ax_age.set_ylabel("Số lượng")
        else:
            self.ax_age.text(0.5, 0.5, "Không có dữ liệu", horizontalalignment='center')
        self.canvas.draw()
        logger.info("Charts updated with current student data.")


class StudentPage(formPage):
    """
    Page for managing student information.

    Inherits from formPage to provide a table view with search and filter capabilities.
    """
    def __init__(self, main_stack=None):
        """
        Initializes the StudentPage.
        
        Args:
            main_stack: The QStackedWidget used for navigation.
        """
        self.main_stack = main_stack
        try:
            raw_data = get_preview_data(GET_PREVIEW_STUDENT_DATA_QUERY)
            self.preview_data = get_right_table_data_form(raw_data)
            logger.info("Student preview data loaded successfully.")
        except Exception as e:
            logger.error("Error loading student preview data: %s", e)
            self.preview_data = []
        super().__init__(
            self.preview_data,
            field=["Chọn", "ID", "Tên", "Giới tính", "Ngày sinh"],
            title="Quản lý học sinh",
            main_stack=self.main_stack,
            search_text="Tìm kiếm học sinh",
            filter_fields=["ID", "Tên", "Giới tính", "Ngày sinh"],
            single_select=True
        )
    
    def delete(self):
        """
        Deletes selected student rows using the external delete() function.
        """
        return delete(self)
    
    def go_to_add_page(self):
        """
        Navigates to the AddStudentPage.
        """
        if self.main_stack:
            add_page = AddStudentPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
            logger.info("Navigated to AddStudentPage.")
        else:
            logger.error("Main stack not provided for navigation!")
    
    def go_to_edit_page(self):
        """
        Navigates to the AlterStudentPage for the selected student.
        """
        student_id = self.get_id_selected()
        if student_id is None:
            logger.warning("No student selected for editing.")
            return
        if self.main_stack:
            edit_page = AlterStudentPage(parent_stack=self.main_stack, student_id=student_id)
            self.main_stack.addWidget(edit_page)
            self.main_stack.setCurrentWidget(edit_page)
            logger.info("Navigated to AlterStudentPage for student ID: %s", student_id)
        else:
            logger.error("Main stack not provided for navigation!")


class GradesPage(formPage):
    """
    Page for managing student grades.
    """
    def __init__(self, main_stack=None):
        """
        Initializes the GradesPage.
        
        Args:
            main_stack: The QStackedWidget used for navigation.
        """
        self.main_stack = main_stack
        try:
            raw_data = get_preview_data(GET_GRADES_DATA_QUERY)
            self.preview_data = get_right_table_data_form(raw_data)
            logger.info("Grades preview data loaded successfully.")
        except Exception as e:
            logger.error("Error loading grades preview data: %s", e)
            self.preview_data = []
        super().__init__(
            self.preview_data,
            field=["Chọn", "ID", "Tên", "Điểm"],
            title="Quản lý điểm",
            main_stack=self.main_stack,
            search_text="Tìm kiếm học sinh",
            filter_fields=["ID", "Tên", "Điểm"],
            single_select=True
        )
    
    def go_to_add_page(self):
        """
        Navigates to the AddGradePage.
        """
        if self.main_stack:
            add_page = AddGradePage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
            logger.info("Navigated to AddGradePage.")
        else:
            logger.error("Main stack not provided for navigation!")
    
    def go_to_edit_page(self):
        """
        Navigates to the AltergradesPage for the selected student.
        """
        student_id = self.get_id_selected()
        if student_id is None:
            logger.warning("No student selected for editing grades.")
            return
        if self.main_stack:
            edit_page = AltergradesPage(parent_stack=self.main_stack, student_id=student_id)
            self.main_stack.addWidget(edit_page)
            self.main_stack.setCurrentWidget(edit_page)
            logger.info("Navigated to AltergradesPage for student ID: %s", student_id)
        else:
            logger.error("Main stack not provided for navigation!")
    
    def delete(self):
        """
        Deletes selected student rows using the external delete() function.
        """
        return delete(self)


class TuitionPage(formPage):
    """
    Page for managing student tuition fees.
    """
    def __init__(self, main_stack=None):
        """
        Initializes the TuitionPage.
        
        Args:
            main_stack: The QStackedWidget used for navigation.
        """
        self.main_stack = main_stack
        try:
            raw_data = get_preview_data(GET_TUITION_DATA_QUERY)
            self.preview_data = get_right_table_data_form(raw_data)
            logger.info("Tuition preview data loaded successfully.")
        except Exception as e:
            logger.error("Error loading tuition preview data: %s", e)
            self.preview_data = []
        super().__init__(
            self.preview_data,
            field=["Chọn", "ID", "Tên", "Học phí", "Đóng"],
            title="Quản lý học phí",
            main_stack=self.main_stack,
            search_text="Tìm kiếm học sinh",
            filter_fields=["ID", "Tên", "Học phí"],
            single_select=True
        )
    
    def go_to_add_page(self):
        """
        Navigates to the AddFeePage.
        """
        if self.main_stack:
            add_page = AddFeePage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
            logger.info("Navigated to AddFeePage.")
        else:
            logger.error("Main stack not provided for navigation!")
    
    def go_to_edit_page(self):
        """
        Navigates to the AlterFeePage for the selected student.
        """
        student_id = self.get_id_selected()
        if student_id is None:
            logger.warning("No student selected for editing tuition.")
            return
        if self.main_stack:
            edit_page = AlterFeePage(parent_stack=self.main_stack, student_id=student_id)
            self.main_stack.addWidget(edit_page)
            self.main_stack.setCurrentWidget(edit_page)
            logger.info("Navigated to AlterFeePage for student ID: %s", student_id)
        else:
            logger.error("Main stack not provided for navigation!")
    
    def delete(self):
        """
        Deletes selected student rows using the external delete() function.
        """
        return delete(self)


