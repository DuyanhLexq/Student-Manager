from GUI.util import formPage
from GUI.Class.addClass_func import AddClassPage
class classPage(formPage):
    def __init__(self, main_stack=None):
        """
        main_stack: QStackedWidget chứa các trang của ứng dụng, dùng để chuyển trang.
        """
        self.main_stack = main_stack
        super().__init__(
            [
            ["CLASS001", "Lớp 11-cô Hiền","40","15/03/2024"],
            ["CLASS002", "Lớp 12","40","15/03/2024"],
            ["CLASS003", "Lớp 10","40","15/03/2024"]
        ],
        field= ["Chọn", "ID", "Tên", "Số lượng học sinh", "Ngày tạo"],
        title= "Quản lý lớp",
        main_stack= self.main_stack,
        search_text = "Tìm kiếm học sinh",
        filter_fields = ["ID", "Tên", "Số lượng học sinh", "Ngày tạo"]
        )
    def go_to_add_page(self):
        if self.main_stack:
            add_page = AddClassPage(parent_stack=self.main_stack)
            self.main_stack.addWidget(add_page)
            self.main_stack.setCurrentWidget(add_page)
        else:
            print("Main stack chưa được cung cấp!")