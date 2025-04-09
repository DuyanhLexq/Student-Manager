-- Chèn dữ liệu mẫu cho giáo viên
INSERT INTO teachers (teacher_name, phone, hometown, start_date, contract_end_date, birth_date) VALUES
('Nguyễn Văn An', '0987654321', 'Hà Nội', '2020-05-01', '2023-05-01', '1985-03-15'),
('Trần Thị Bình', '0912345678', 'Đà Nẵng', '2021-06-01', '2024-06-01', '1990-07-20'),
('Lê Văn Cường', '0967890123', 'TP HCM', '2022-02-15', '2025-02-15', '1988-11-30');

-- Chèn dữ liệu mẫu cho lớp học
INSERT INTO classes (class_name, creation_date, student_count, teacher_id) VALUES
('Toán 10', '2022-09-01', 30, 1),
('Văn 9', '2023-01-10', 25, 2),
('Anh 8', '2023-03-05', 28, 3);

-- Chèn dữ liệu mẫu cho học sinh
INSERT INTO students (student_name, phone, parent_phone, parent_name, hometown, temporary_address, birth_date, gender, class_id) VALUES
('Phạm Duy Minh', '0987123456', '0912345678', 'Nguyễn Thị Hà', 'Hà Nội', 'Số 1 Đường ABC, Hà Nội', '2010-05-10', 'Nam', 1),
('Lê Thị Hương', '0978123456', '0987654321', 'Lê Văn Đức', 'Hải Phòng', 'Số 2 Đường XYZ, Hải Phòng', '2009-08-12', 'Nữ', 1),
('Trần Văn Tú', '0965874123', '0911472583', 'Trần Thị Mai', 'Hà Nội', 'Số 5 Đường DEF, Hà Nội', '2011-02-28', 'Nam', 1),
('Hoàng Thị Lan', '0936147258', '0978365142', 'Hoàng Văn Sơn', 'Đà Nẵng', 'Số 3 Đường KLM, Đà Nẵng', '2008-11-05', 'Nữ', 2),
('Nguyễn Văn Dũng', '0918754632', '0963524178', 'Nguyễn Thị Thu', 'TP HCM', 'Số 7 Đường QWER, TP HCM', '2009-07-19', 'Nam', 2),
('Vũ Thị Hà', '0987654321', '0918273645', 'Vũ Văn Hải', 'Đà Nẵng', 'Số 8 Đường RTY, Đà Nẵng', '2010-12-25', 'Nữ', 2),
('Phan Văn Hoàng', '0975314682', '0987123456', 'Phan Thị Hồng', 'Hà Nội', 'Số 10 Đường UVW, Hà Nội', '2011-06-15', 'Nam', 3),
('Lý Thị Mai', '0963258741', '0912345678', 'Lý Văn Minh', 'TP HCM', 'Số 12 Đường OPQ, TP HCM', '2008-04-30', 'Nữ', 3),
('Đỗ Văn Sơn', '0936251478', '0978123456', 'Đỗ Thị Lan', 'Hải Phòng', 'Số 15 Đường ASD, Hải Phòng', '2009-09-09', 'Nam', 3),
('Trịnh Thu Thủy', '0936251478', '0978123456', 'Đỗ Thị Lan', 'Hải Phòng', 'Số 15 Đường ASD, Hải Phòng', '2009-09-09', 'Nữ', NULL);

-- Chèn dữ liệu lương giáo viên
INSERT INTO salary (teacher_id, salary, bonus_salary) VALUES
(1, 20000000.00, 5000000.00),
(2, 18000000.00, 4500000.00),
(3, 22000000.00, 6000000.00);

-- Chèn dữ liệu điểm học sinh
INSERT INTO scores (student_id, score) VALUES
(1, 8.5),
(2, 9.0),
(3, 7.5),
(4, 8.0),
(5, 8.8),
(6, 9.2),
(7, 7.0),
(8, 8.9),
(9, 9.5);

-- Chèn dữ liệu học phí
INSERT INTO tuition (student_id, fee, paid) VALUES
(1, 5000000.00, TRUE),
(2, 5000000.00, FALSE),
(3, 5000000.00, TRUE),
(4, 5000000.00, TRUE),
(5, 5000000.00, FALSE),
(6, 5000000.00, TRUE),
(7, 5000000.00, FALSE),
(8, 5000000.00, TRUE),
(9, 5000000.00, FALSE);