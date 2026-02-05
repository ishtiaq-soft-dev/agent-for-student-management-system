from langchain.tools import tool
from src.models.model import Student
from src.extensions.extension import db

@tool(description="Use this tool for Create a new student in the database. Requires name, email, department and age.")
def create_student(name: str, email: str, department: str, age: int) -> Student:

    '''
    Create a new student in the database.
    
    args:
        name (str): The name of the student.
        email (str): The email of the student.
        department (str): The department of the student.
        age (int): The age of the student.
    '''

    errors = []

    if not name:
        errors.append("Name is required.")
    if not email:
        errors.append("Email is required.")
    if not department:
        errors.append("Department is required.")
    if not age:
        errors.append("Age is required.")
    if errors:
        raise ValueError(" ".join(errors))
    

    new_student = Student(name=name, email=email, department=department, age=age)
    db.session.add(new_student)
    db.session.commit()
    return f"student {name} created successfully with email {email}, department {department} and age {age}."

@tool(description="Use this tool for Update an existing student in the database. Requires student_id and any of the following: name, email, department or age.")
def update_student(student_id: int, name: str = None, email: str = None, department: str = None, age: int = None) -> Student:
    '''
    Update an existing student in the database.
    
    args:
        student_id (int): The ID of the student to update.
        name (str): The new name of the student (optional).
        email (str): The new email of the student (optional).
        department (str): The new department of the student (optional).
        age (int): The new age of the student (optional).
    '''
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with ID {student_id} not found.")
    
    if name:
        student.name = name
    if email:
        student.email = email
    if department:
        student.department = department
    if age:
        student.age = age
    
    db.session.commit()
    return f"student with ID {student_id} updated successfully."

@tool(description="Use this tool for Delete an existing student from the database. Requires student_id.")
def delete_student(student_id: int) -> Student:
    '''
    Delete an existing student from the database.
    
    args:
        student_id (int): The ID of the student to delete.
    '''
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with ID {student_id} not found.")
    
    db.session.delete(student)
    db.session.commit()
    return f"student with ID {student_id} deleted successfully."

@tool(description="Use this tool for Get an existing student from the database. Requires student_id.")
def get_student(student_id: int) -> Student:
    '''
    Get an existing student from the database.
    
    args:
        student_id (int): The ID of the student to get.
    '''
    student = Student.query.get(student_id)
    if not student:
        raise ValueError(f"Student with ID {student_id} not found.")
    
    return student.to_dict()

@tool(description="Use this tool for Get all students from the database.")
def get_all_students() -> list:
    '''
    Get all students from the database.
    '''
    students = Student.query.all()
    return [student.to_dict() for student in students]

@tool(description="Use this tool for Get the count of students in the database.")
def get_students_count() -> int:
    '''
    Get the count of students in the database.
    '''
    return Student.query.count()

list_of_tools = [create_student, update_student, delete_student, get_student, get_all_students, get_students_count]