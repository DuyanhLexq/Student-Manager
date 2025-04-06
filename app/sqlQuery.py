# Các truy vấn hiện có (cần sửa lại truy vấn lương)
GET_PREVIEW_TEACHER_DATA_QUERY = """
    SELECT teacher_id, teacher_name, birth_date, start_date
    FROM teachers;
"""

GET_PREVIEW_SALARY_DATA_QUERY = """
    SELECT t.teacher_id, t.teacher_name, s.salary, s.bonus_salary
    FROM teachers t
    JOIN salary s ON t.teacher_id = s.teacher_id;
"""

GET_PREVIEW_STUDENT_DATA_QUERY = """
    SELECT student_id, student_name, gender, birth_date
    FROM students;
"""

# Bổ sung các truy vấn mới
GET_GRADES_DATA_QUERY = """
    SELECT st.student_id, st.student_name, sc.score
    FROM students st
    JOIN scores sc ON st.student_id = sc.student_id;
"""

GET_TUITION_DATA_QUERY = """
    SELECT st.student_id, 
           st.student_name, 
           t.fee, 
           CASE 
               WHEN t.paid = 1 THEN 'Đã đóng' 
               ELSE 'Chưa đóng' 
           END AS paid_status
    FROM students st
    JOIN tuition t ON st.student_id = t.student_id;
"""