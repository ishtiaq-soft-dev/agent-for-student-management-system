from flask import Blueprint, request, jsonify
from .agent import initialize_agent


chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/chat', methods=['POST', 'GET'])
def chat():

    data = request.get_json()
    user_message = data.get('message', '')

    agent = initialize_agent()
    
    response = agent.invoke({
        "messages": [{"role": "user", "content": user_message}]
    })

    return jsonify({"response": response['messages'][-1].content})