from flask import Blueprint, request, jsonify, render_template
from .agent import initialize_agent
from src.models.model import Student
from src.extensions.extension import db


chatbot_bp = Blueprint('chatbot', __name__)


@chatbot_bp.route('/')
def index():
    return render_template('index.html')


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({"response": "Please provide a message."}), 400
        
        agent = initialize_agent()
        
        response = agent.invoke({
            "messages": [{"role": "user", "content": user_message}]
        })
        
        return jsonify({"response": response['messages'][-1].content})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"}), 500


# --- Student REST endpoints for direct CRUD operations ---
@chatbot_bp.route('/api/students', methods=['GET'])
def api_get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


@chatbot_bp.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student.to_dict())


@chatbot_bp.route('/api/students', methods=['POST'])
def api_create_student():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    department = data.get('department')
    age = data.get('age')
    if not all([name, email, department, age]):
        return jsonify({'error': 'Missing required fields'}), 400
    new_student = Student(name=name, email=email, department=department, age=age)
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201


@chatbot_bp.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    data = request.get_json() or {}
    for field in ('name', 'email', 'department', 'age'):
        if field in data:
            setattr(student, field, data[field])
    db.session.commit()
    return jsonify(student.to_dict())


@chatbot_bp.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'deleted'})


@chatbot_bp.route('/api/students/count', methods=['GET'])
def api_students_count():
    count = Student.query.count()
    return jsonify({'count': count})