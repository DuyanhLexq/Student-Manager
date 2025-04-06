import sqlite3
from sqlQuery import *
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

