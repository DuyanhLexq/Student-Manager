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
    LEFT JOIN 
        teachers ON classes.teacher_id = teachers.teacher_id
    LEFT JOIN 
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

CHECK_STUDENT_NAME_QUERY = """
    SELECT 
        student_id
    FROM 
        students
    WHERE 
        student_name = '{}'
    ORDER BY 
        student_id ASC
    LIMIT 1;
"""
CHECK_TEACHER_NAME_QUERY =  """
    SELECT 
        teacher_id
    FROM 
        teachers
    WHERE 
        teacher_name = '{}'
    ORDER BY 
        teacher_id ASC
    LIMIT 1;
"""

ADD_STUDENT_QUERY = """
    INSERT INTO students (
        student_name, 
        phone, 
        parent_phone, 
        parent_name, 
        hometown, 
        temporary_address, 
        birth_date, 
        gender, 
        class_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ADD_SCORE_QUERY = """
    INSERT INTO scores (student_id, score)
    VALUES (?, ?)
"""

ADD_TUITION_QUERY = """
    INSERT INTO tuition (student_id, fee, paid)
    VALUES (?, ?, ?)
"""
ADD_TEACHER_QUERY = """
    INSERT INTO teachers (
        teacher_name, 
        phone, 
        hometown, 
        start_date, 
        contract_end_date, 
        birth_date
    ) VALUES (?, ?, ?, ?, ?, ?);
"""

ADD_SALARY_QUERY = """
    INSERT INTO salary (
        teacher_id,
        salary,
        bonus_salary
    ) VALUES (?, ?, ?);
"""
ADD_CLASS_QUERY = """
    INSERT INTO classes (
        class_name,
        creation_date,
        student_count,
        teacher_id
    ) VALUES (?, ?, ?, ?);
"""
ASSIGN_STUDENTS_TO_CLASS_QUERY = """
UPDATE students
SET class_id = ?
WHERE student_id IN ({});
"""

UPDATE_STUDENT_QUERY = """
    UPDATE students
    SET 
        student_name = ?,
        phone = ?,
        parent_phone = ?,
        parent_name = ?,
        hometown = ?,
        temporary_address = ?,
        birth_date = ?,
        gender = ?
    WHERE student_id = ?;
"""

UPDATE_TUITION_QUERY = """
    UPDATE tuition
    SET 
        fee = ?,
        paid = ?
    WHERE student_id = ?;
"""
UPDATE_GRADE_QUERY = """
    UPDATE scores
    SET 
        score = ?
    WHERE student_id = ?;
"""

UPDATE_TEACHER_QUERY = """
    UPDATE teachers
    SET 
        teacher_name = ?,
        phone = ?,
        hometown = ?,
        start_date = ?,
        contract_end_date = ?,
        birth_date = ?
    WHERE teacher_id = ?;

"""

UPDATE_SALARY_QUERY = """
    UPDATE salary
    SET 
        salary = ?,
        bonus_salary = ?
    WHERE teacher_id = ?;
"""

UPDATE_CLASS_AND_STUDENTS_QUERY = {
    "update_class": """
        UPDATE classes
        SET class_name = ?, student_count = ?, teacher_id = ?
        WHERE class_id = ?;
    """,
    "assign_students_to_class": """
        UPDATE students
        SET class_id = ?
        WHERE student_id IN ({student_ids});
    """,
    "unassign_students_not_in_list": """
        UPDATE students
        SET class_id = NULL
        WHERE class_id = ? AND student_id NOT IN ({student_ids});
    """,
    "remove_all_students_from_class": """
        UPDATE students
        SET class_id = NULL
        WHERE class_id = ?;
    """
}
