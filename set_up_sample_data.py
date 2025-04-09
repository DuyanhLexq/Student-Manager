import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite (nếu chưa có sẽ tạo mới)
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Danh sách các bảng sẽ kiểm tra và xóa nếu có
tables = ["tuition", "scores", "salary", "students", "classes", "teachers"]

# Xóa bảng nếu tồn tại (phải xóa theo thứ tự để tránh lỗi foreign key)
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
# Tạo lại các bảng
with open("sql-Query/create_table_sqlite.sql", "r",encoding='utf-8') as f:
    sql_script_cr = f.read()
with open("sql-Query/insert_sample_data_sqlite.sql", "r",encoding='utf-8') as f:
    sql_script_in = f.read()
cursor.executescript(sql_script_cr)
cursor.executescript(sql_script_in)


conn.commit()
conn.close()

print("Đã kiểm tra, xóa nếu tồn tại và tạo mới lại tất cả các bảng.")
