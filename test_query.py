
GET_PREVIEW_CLASSES_DATA_QUERY = """
    SELECT 
        class_id,
        class_name,
        student_count,
        creation_date
    FROM 
        classes;
"""


import sqlite3
from typing import List
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

def get_right_table_data_form(data: List[tuple[str]]) -> List[List[str]]:
    res = []
    for dt in data:
        accurate_data = list(map(lambda value: str(value), dt))
        res.append(accurate_data)
    return res


print(get_right_table_data_form(get_preview_data(GET_PREVIEW_CLASSES_DATA_QUERY)))
    