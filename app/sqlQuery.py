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

GET_PREVIEW_CLASSES_DATA_QUERY = """
    SELECT 
        class_id,
        class_name,
        student_count,
        creation_date
    FROM 
        classes;
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

GET_STUDENT_INFO_BY_ID_QUERY = """
    SELECT student_name,
           gender,
           birth_date,
           hometown,
           temporary_address,
           parent_name,
           phone,
           parent_phone
    FROM students
    WHERE student_id = {};
"""

GET_GRADES_DATA_BY_ID_QUERY = """
    SELECT 
        students.student_name,
        scores.score
    FROM 
        students
    JOIN 
        scores ON students.student_id = scores.student_id
    WHERE 
        students.student_id = {};
"""

GET_TUITION_DATA_BY_ID_QUERY = """
    SELECT 
        students.student_name,
        tuition.fee,
        CASE 
            WHEN tuition.paid = TRUE THEN 'Đã đóng'
            ELSE 'Chưa đóng'

        END AS payment_status
    FROM 
        students
    JOIN 
        tuition ON students.student_id = tuition.student_id
    WHERE 
        students.student_id = {};
"""

GET_TEACHER_DATA_BY_ID_QUERY = """
    SELECT 
        teacher_name,
        birth_date,
        phone,
        contract_end_date,
        start_date,
        hometown
    FROM 
        teachers
    WHERE 
        teacher_id = {};
"""

GET_CLASS_DATA_BY_ID_QUERY = """
    SELECT 
        classes.class_name,
        classes.student_count,
        classes.creation_date,
        classes.teacher_id,
        GROUP_CONCAT(students.student_id)
    FROM 
        classes
    JOIN 
        teachers ON classes.teacher_id = teachers.teacher_id
    JOIN 
        students ON students.class_id = classes.class_id
    WHERE 
        classes.class_id = {}
    GROUP BY 
        classes.class_id;

"""

GET_SALARY_DATA_BY_ID_QUERY = """
    SELECT 
        teachers.teacher_name,
        salary.salary,
        salary.bonus_salary
    FROM 
        teachers
    JOIN 
        salary ON teachers.teacher_id = salary.teacher_id
    WHERE 
        teachers.teacher_id = {};
"""