import uuid

STUDENTS_DB = {}

def create_student(profile):
    student_id = str(uuid.uuid4())
    STUDENTS_DB[student_id] = profile
    return student_id

def get_student(student_id):
    return STUDENTS_DB.get(student_id)
