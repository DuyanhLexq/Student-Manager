import sqlite3

# Kết nối đến cơ sở dữ liệu SQLite (nếu chưa có sẽ tạo mới)
conn = sqlite3.connect('student_management.db')
cursor = conn.cursor()

# Bật chế độ kiểm tra foreign key
cursor.execute("PRAGMA foreign_keys = ON;")
# Tạo bảng giáo viên (teachers)
cursor.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    hometown TEXT NOT NULL,
    start_date TEXT NOT NULL,
    contract_end_date TEXT NOT NULL,
    birth_date TEXT NOT NULL
);
''')

# Tạo bảng lớp học (classes)
cursor.execute('''
CREATE TABLE IF NOT EXISTS classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    student_count INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);
''')

# Tạo bảng học sinh (students)
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    phone TEXT,
    parent_phone TEXT NOT NULL,
    parent_name TEXT NOT NULL,
    hometown TEXT NOT NULL,
    temporary_address TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    gender TEXT NOT NULL,
    class_id INTEGER NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);
''')

# Tạo bảng lương giáo viên (salary)
cursor.execute('''
CREATE TABLE IF NOT EXISTS salary (
    teacher_id INTEGER NOT NULL,
    salary REAL NOT NULL,
    bonus_salary REAL NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);
''')

# Tạo bảng điểm học sinh (scores)
cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    student_id INTEGER NOT NULL,
    score REAL NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
''')

# Tạo bảng học phí (tuition)
cursor.execute('''
CREATE TABLE IF NOT EXISTS tuition (
    student_id INTEGER NOT NULL,
    fee REAL NOT NULL,
    paid BOOLEAN NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
''')

# Chèn dữ liệu mẫu cho giáo viên
cursor.executemany('''
INSERT INTO teachers (teacher_name, phone, hometown, start_date, contract_end_date, birth_date) VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('Nguyễn Văn An', '0987654321', 'Hà Nội', '2020-05-01', '2023-05-01', '1985-03-15'),
    ('Trần Thị Bình', '0912345678', 'Đà Nẵng', '2021-06-01', '2024-06-01', '1990-07-20'),
    ('Lê Văn Cường', '0967890123', 'TP HCM', '2022-02-15', '2025-02-15', '1988-11-30')
])

# Chèn dữ liệu mẫu cho lớp học
cursor.executemany('''
INSERT INTO classes (class_name, creation_date, student_count, teacher_id) VALUES (?, ?, ?, ?)
''', [
    ('Toán 10', '2022-09-01', 30, 1),
    ('Văn 9', '2023-01-10', 25, 2),
    ('Anh 8', '2023-03-05', 28, 3)
])

# Chèn dữ liệu mẫu cho học sinh
cursor.executemany('''
INSERT INTO students (student_name, phone, parent_phone, parent_name, hometown, temporary_address, birth_date, gender, class_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [
    ('Phạm Duy Minh', '0987123456', '0912345678', 'Nguyễn Thị Hà', 'Hà Nội', 'Số 1 Đường ABC, Hà Nội', '2010-05-10', 'Nam', 1),
    ('Lê Thị Hương', '0978123456', '0987654321', 'Lê Văn Đức', 'Hải Phòng', 'Số 2 Đường XYZ, Hải Phòng', '2009-08-12', 'Nữ', 1),
    ('Trần Văn Tú', '0965874123', '0911472583', 'Trần Thị Mai', 'Hà Nội', 'Số 5 Đường DEF, Hà Nội', '2011-02-28', 'Nam', 1),
    ('Hoàng Thị Lan', '0936147258', '0978365142', 'Hoàng Văn Sơn', 'Đà Nẵng', 'Số 3 Đường KLM, Đà Nẵng', '2008-11-05', 'Nữ', 2),
    ('Nguyễn Văn Dũng', '0918754632', '0963524178', 'Nguyễn Thị Thu', 'TP HCM', 'Số 7 Đường QWER, TP HCM', '2009-07-19', 'Nam', 2),
    ('Vũ Thị Hà', '0987654321', '0918273645', 'Vũ Văn Hải', 'Đà Nẵng', 'Số 8 Đường RTY, Đà Nẵng', '2010-12-25', 'Nữ', 2),
    ('Phan Văn Hoàng', '0975314682', '0987123456', 'Phan Thị Hồng', 'Hà Nội', 'Số 10 Đường UVW, Hà Nội', '2011-06-15', 'Nam', 3),
    ('Lý Thị Mai', '0963258741', '0912345678', 'Lý Văn Minh', 'TP HCM', 'Số 12 Đường OPQ, TP HCM', '2008-04-30', 'Nữ', 3),
    ('Đỗ Văn Sơn', '0936251478', '0978123456', 'Đỗ Thị Lan', 'Hải Phòng', 'Số 15 Đường ASD, Hải Phòng', '2009-09-09', 'Nam', 3)
])

# Chèn dữ liệu lương giáo viên
cursor.executemany('''
INSERT INTO salary (teacher_id, salary, bonus_salary) VALUES (?, ?, ?)
''', [
    (1, 20000000.00, 5000000.00),
    (2, 18000000.00, 4500000.00),
    (3, 22000000.00, 6000000.00)
])

# Chèn dữ liệu điểm học sinh
cursor.executemany('''
INSERT INTO scores (student_id, score) VALUES (?, ?)
''', [
    (1, 8.5),
    (2, 9.0),
    (3, 7.5),
    (4, 8.0),
    (5, 8.8),
    (6, 9.2),
    (7, 7.0),
    (8, 8.9),
    (9, 9.5)
])

# Chèn dữ liệu học phí
cursor.executemany('''
INSERT INTO tuition (student_id, fee, paid) VALUES (?, ?, ?)
''', [
    (1, 5000000.00, True),
    (2, 5000000.00, False),
    (3, 5000000.00, True),
    (4, 5000000.00, True),
    (5, 5000000.00, False),
    (6, 5000000.00, True),
    (7, 5000000.00, False),
    (8, 5000000.00, True),
    (9, 5000000.00, False)
])

# Commit các thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Cơ sở dữ liệu đã được tạo và dữ liệu đã được chèn vào thành công.")
