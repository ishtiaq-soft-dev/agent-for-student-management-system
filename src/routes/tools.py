from langchain.tools import tool
from src.models.model import Student
from src.extensions.extension import db
from src.utils.formatter import format_markdown_table, format_markdown_table_multiple

@tool(description="Create a new student record.")
def create_student(name: str, email: str, department: str, age: int) -> str:
    '''
    Docstring for create_student
    
    :param name: Description
    :type name: str
    :param email: Description
    :type email: str
    :param department: Description
    :type department: str
    :param age: Description
    :type age: int
    :return: Description
    :rtype: str
    '''
    new_student = Student(name=name, email=email, department=department, age=age)
    db.session.add(new_student)
    db.session.commit()
    
    # Format response with table
    student_data = new_student.to_dict()
    table = format_markdown_table(student_data)
    return f"✅ **Student record created successfully!**\n\n{table}"

@tool(description="Update an existing student record.")
def update_student(student_id: int, name: str = None, email: str = None, department: str = None, age: int = None) -> str:
     '''
        Docstring for update_student
        :param student_id: Description
        :type student_id: int
        :param name: Description
        :type name: str
        :param email: Description
        :type email: str
        :param department: Description
        :type department: str
        :param age: Description
        :type age: int
        :return: Description
        :rtype: str

     '''
     student = Student.query.get(student_id)
     if not student:
          return f"❌ Student with ID {student_id} not found."
     if name:
          student.name = name
     if email:
          student.email = email
     if department:
          student.department = department
     if age:
          student.age = age
     db.session.commit()
     
     # Return updated student info in table format
     student_data = student.to_dict()
     table = format_markdown_table(student_data)
     return f"✏️ **Student {student_id} updated successfully!**\n\n{table}"

@tool(description="Delete a student record.")
def delete_student(student_id: int) -> str:
    '''
    Docstring for delete_student
    :param student_id: Description
    :type student_id: int
    :return: Description
    :rtype: str

    '''
    student = Student.query.get(student_id)
    if not student:
        return f"❌ Student with ID {student_id} not found."
    
    student_name = student.name
    db.session.delete(student)
    db.session.commit()
    return f"🗑️ **Student {student_name} (ID: {student_id}) deleted successfully!**"

@tool(description="Retrieve a student record by ID.")
def get_student(student_id: int) -> str:
    '''
    Docstring for get_student
    :param student_id: Description
    :type student_id: int
    :return: Description
    :rtype: str

    '''
    student = Student.query.get(student_id)
    if not student:
        return f"❌ Student with ID {student_id} not found."
    
    student_data = student.to_dict()
    table = format_markdown_table(student_data)
    return f"📋 **Student Record (ID: {student_id})**\n\n{table}"

@tool(description="Retrieve all student records.")
def get_all_students() -> str:
    '''
    Docstring for get_all_students
    :return: Description
    :rtype: str
    '''
    students = Student.query.all()
    students_list = [student.to_dict() for student in students]
    
    if not students_list:
        return "📊 No students found in the database."
    
    table = format_markdown_table_multiple(students_list)
    return f"📊 **All Students ({len(students_list)} records)**\n\n{table}"

@tool(description="Get the total count of student records.")
def get_students_count() -> str:
    '''
    Docstring for get_students_count
    :return: Description
    :rtype: str
    '''
    count = Student.query.count()
    return f"📊 Total student records: **{count}**"

list_of_tools = [create_student, update_student, delete_student, get_student, get_all_students, get_students_count]