CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    hometown VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    contract_end_date DATE NOT NULL,
    birth_date DATE NOT NULL
);

CREATE TABLE classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL,
    creation_date DATE NOT NULL,
    student_count INT NOT NULL,
    teacher_id INT NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    parent_phone VARCHAR(20) NOT NULL,
    parent_name VARCHAR(255) NOT NULL,
    hometown VARCHAR(255) NOT NULL,
    temporary_address VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    class_id INT NOT NULL,
    FOREIGN KEY (class_id) REFERENCES classes(class_id)
);

-- Tạo bảng lương
CREATE TABLE salary (
    teacher_id INT NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    bonus_salary DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
);

-- Tạo bảng điểm
CREATE TABLE scores (
    student_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Tạo bảng học phí
CREATE TABLE tuition (
    student_id INT NOT NULL,
    fee DECIMAL(10,2) NOT NULL,
    paid BOOLEAN NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);
