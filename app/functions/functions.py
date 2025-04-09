import sqlite3
from sqlQuery import *
from typing import List, Tuple
def open_db_connection():
    """
    Open a connection to the SQLite database.
    """
    try:
        # Kết nối đến file SQLite. Nếu file không tồn tại thì sẽ được tạo mới.
        conn = sqlite3.connect(r"C:\Project_Python\applications\Student-Manager\student_management.db")
        return conn
    except sqlite3.Error as e:
        print("Không thể kết nối cơ sở dữ liệu:", e)
        return None

def execute_query(QUERY:str,*args) -> None:
    """
    Execute a given SQL query on the SQLite database.
    Trả về None nếu không có lỗi, ngược lại trả về thông báo lỗi.
    """
    conn = open_db_connection()
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute(QUERY,tuple(args)) # Thực thi truy vấn với các tham số
        # Nếu có thay đổi dữ liệu, commit lại
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as e:
        print("Lỗi truy vấn:", e)
        conn.close()


def get_preview_data(QUERY:str):
    """
    Query to get teacher data using sqlite3.
    Trả về danh sách tuple chứa: (teacher_id, teacher_name, birth_date, start_date)
    """
    conn = open_db_connection()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(QUERY)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except sqlite3.Error as e:
        print("Lỗi truy vấn:", e)
        conn.close()
        return []

def add_new_student(student_data: List) -> None:
    conn = open_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(ADD_STUDENT_QUERY, (*student_data, None))
        conn.commit()
        # Lấy ID của học sinh mới được thêm vào
        new_student_id = cursor.lastrowid

        cursor.execute(ADD_TUITION_QUERY, (new_student_id, None, None))
        cursor.execute(ADD_SCORE_QUERY, (new_student_id, None))

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã thêm học sinh mới với ID {new_student_id}")
    except sqlite3.Error as e:
        print("Lỗi khi thêm học sinh:", e)
        conn.close()

def add_new_teacher(teacher_data: List) -> None:
    conn = open_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(ADD_TEACHER_QUERY, (*teacher_data,))
        conn.commit()
        # Lấy ID của giáo viên mới được thêm vào
        new_teacher_id = cursor.lastrowid
        cursor.execute(ADD_SALARY_QUERY, (new_teacher_id, None,None))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã thêm giáo viên mới với ID {new_teacher_id}")
    except sqlite3.Error as e:
        print("Lỗi khi thêm giáo viên:", e)
        conn.close()

def add_new_class(class_data: List,id_student_format:str) -> None:
    conn = open_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(ADD_CLASS_QUERY, (*class_data,))
        conn.commit()
        new_class_id = cursor.lastrowid
        cursor.execute(ASSIGN_STUDENTS_TO_CLASS_QUERY.format(id_student_format), (new_class_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã thêm lớp mới với ID {new_class_id}")
    except sqlite3.Error as e:
        print("Lỗi khi thêm lớp:", e)
        conn.close()


def update_student_info(student_id: int, updated_data: List) -> None:
    """
    Cập nhật thông tin học sinh trong cơ sở dữ liệu.
    student_id: ID của học sinh cần cập nhật.
    updated_data: Danh sách chứa các thông tin mới của học sinh.
    """
    conn = open_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_STUDENT_QUERY, (*updated_data, student_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã cập nhật thông tin học sinh với ID {student_id}")
    except sqlite3.Error as e:
        print("Lỗi khi cập nhật thông tin học sinh:", e)
        conn.close()

def update_student_grade(student_id: int, updated_data: List) -> None:
    """
    Cập nhật điểm của học sinh trong cơ sở dữ liệu.
    student_id: ID của học sinh cần cập nhật.
    updated_data: Danh sách chứa các thông tin mới về điểm số của học sinh.
    """
    conn = open_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_GRADE_QUERY, (*updated_data, student_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã cập nhật điểm số của học sinh với ID {student_id}")
    except sqlite3.Error as e:
        print("Lỗi khi cập nhật điểm số:", e)
        conn.close()

def update_student_tuition(student_id: int, updated_data: List) -> None:
    """
    Cập nhật học phí của học sinh trong cơ sở dữ liệu.
    student_id: ID của học sinh cần cập nhật.
    updated_data: Danh sách chứa các thông tin mới về học phí của học sinh.
    """
    conn = open_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_TUITION_QUERY, (*updated_data, student_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã cập nhật học phí của học sinh với ID {student_id}")
    except sqlite3.Error as e:
        print("Lỗi khi cập nhật học phí:", e)
        conn.close()
    
def update_teacher_info(teacher_id: int, updated_data: List) -> None:
    """
    Cập nhật thông tin giáo viên trong cơ sở dữ liệu.
    teacher_id: ID của giáo viên cần cập nhật.
    updated_data: Danh sách chứa các thông tin mới của giáo viên.
    """
    conn = open_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_TEACHER_QUERY, (*updated_data, teacher_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã cập nhật thông tin giáo viên với ID {teacher_id}")
    except sqlite3.Error as e:
        print("Lỗi khi cập nhật thông tin giáo viên:", e)
        conn.close()

def update_teacher_salary(teacher_id: int, updated_data: List) -> None:
    """
    Cập nhật thông tin lương của giáo viên trong cơ sở dữ liệu.
    teacher_id: ID của giáo viên cần cập nhật.
    updated_data: Danh sách chứa các thông tin mới về lương của giáo viên.
    """
    conn = open_db_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_SALARY_QUERY, (*updated_data, teacher_id))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Đã cập nhật lương của giáo viên với ID {teacher_id}")
    except sqlite3.Error as e:
        print("Lỗi khi cập nhật lương:", e)
        conn.close()


def update_class_info(class_id: int, updated_data: List, student_ids: List[int]) -> None:
    """
    Cập nhật thông tin lớp và danh sách học sinh thuộc lớp đó.
    
    Parameters:
    - class_id: ID lớp cần cập nhật.
    - updated_data: [class_name, student_count, teacher_id]
    - student_ids: danh sách ID học sinh thuộc lớp mới.
    """
    conn = open_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()

        # 1. Cập nhật thông tin lớp
        cursor.execute(
            UPDATE_CLASS_AND_STUDENTS_QUERY["update_class"],
            (*updated_data, class_id)
        )

        # 2. Gán class_id cho học sinh trong danh sách mới
        if student_ids:
            cursor.execute(
                UPDATE_CLASS_AND_STUDENTS_QUERY["assign_students_to_class"].format(
                    student_ids=",".join("?" * len(student_ids))
                ),
                (class_id, *student_ids)
            )

            # 3. Gỡ class_id khỏi học sinh không còn thuộc lớp
            cursor.execute(
                UPDATE_CLASS_AND_STUDENTS_QUERY["unassign_students_not_in_list"].format(
                    student_ids=",".join("?" * len(student_ids))
                ),
                (class_id, *student_ids)
            )
        else:
            # Nếu không có học sinh nào trong danh sách mới, gỡ toàn bộ học sinh khỏi lớp
            cursor.execute(
                UPDATE_CLASS_AND_STUDENTS_QUERY["remove_all_students_from_class"],
                (class_id,)
            )

        conn.commit()
        print(f"✅ Đã cập nhật lớp {class_id} và danh sách học sinh.")
    except sqlite3.Error as e:
        print("❌ Lỗi khi cập nhật thông tin lớp:", e)
    finally:
        conn.close()



