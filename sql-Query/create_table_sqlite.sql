CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY,
    teacher_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    hometown TEXT NOT NULL,
    start_date DATE NOT NULL,
    contract_end_date DATE NOT NULL,
    birth_date DATE NOT NULL
);

CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY,
    class_name TEXT NOT NULL,
    creation_date DATE NOT NULL,
    student_count INTEGER NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    phone TEXT,
    parent_phone TEXT NOT NULL,
    parent_name TEXT NOT NULL,
    hometown TEXT NOT NULL,
    temporary_address TEXT NOT NULL,
    birth_date DATE NOT NULL,
    gender TEXT NOT NULL,
    class_id INTEGER,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

CREATE TABLE salary (
    teacher_id INTEGER NOT NULL,
    salary REAL,
    bonus_salary REAL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE scores (
    student_id INTEGER NOT NULL,
    score REAL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE TABLE tuition (
    student_id INTEGER NOT NULL,
    fee REAL,
    paid INTEGER, -- dùng 0/1 thay vì BOOLEAN
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
