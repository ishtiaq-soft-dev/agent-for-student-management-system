# Student Bot Flask 🤖

A Flask-based AI chatbot for managing student records using LangChain and Groq API. The bot can create, retrieve, update, and delete student information through natural language conversations.

## Features ✨

- **AI-Powered Chatbot**: Uses Groq's API with LangChain for intelligent student management
- **CRUD Operations**: Create, Read, Update, and Delete student records
- **Natural Language Interface**: Interact with the bot using plain English
- **Formatted Responses**: Student data displayed in clean markdown tables
- **Database Integration**: SQLAlchemy ORM with Flask-SQLAlchemy
- **RESTful API**: Simple Flask endpoints for chat interactions
- **Error Handling**: Comprehensive error messages with emojis for clarity

## Tech Stack 🛠️

- **Frontend/API**: Flask
- **Database**: SQLAlchemy (SQLite)
- **AI/LLM**: LangChain + Groq API
- **Language**: Python 3.8+
- **Package Manager**: pip

## Prerequisites 📋

- Python 3.8 or higher
- pip (Python package manager)
- Groq API Key (get from [console.groq.com](https://console.groq.com))

## Installation 🚀

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Student_Bot_flask
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
FLASK_DEBUG=true
FLASK_ENV=development
```

### 5. Initialize Database
```bash
python
>>> from src import create_app
>>> app = create_app()
>>> with app.app_context():
...     from src.extensions.extension import db
...     db.create_all()
>>> exit()
```

### 6. Run the Application
```bash
flask run --debug
```

The application will start on `http://localhost:5000`

## Project Structure 📁

```
Student_Bot_flask/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
└── src/
    ├── __init__.py            # Flask app factory
    ├── extensions/
    │   ├── __init__.py
    │   └── extension.py       # Database initialization
    ├── models/
    │   ├── __init__.py
    │   └── model.py           # Student model
    ├── routes/
    │   ├── __init__.py
    │   ├── agent.py           # LangChain agent setup
    │   ├── chatbot_route.py   # Chat endpoint
    │   ├── tools.py           # Student management tools
    │   └── tools2.py          # Additional tools (if any)
    └── utils/
        ├── __init__.py
        └── formatter.py       # Response formatting utilities
```

## API Endpoints 🔌

### Create Student via Chat
**POST** `/chat`

Request:
```json
{
  "message": "Create a new student named Ishtiaq Ahmad, age 28, department BSSE, email ktkishtiaq@gmail.com"
}
```

Response:
```json
{
  "response": "✅ **Student record created successfully!**\n\n| Field | Value |\n|-------|-------|\n| **Id** | 1 |\n| **Name** | Ishtiaq Ahmad |\n..."
}
```

### Get All Students
**POST** `/chat`

Request:
```json
{
  "message": "Show me all students"
}
```

Response: Markdown table with all student records

### Get Student by ID
**POST** `/chat`

Request:
```json
{
  "message": "Show student 1"
}
```

Response: Markdown table with single student's data

### Update Student
**POST** `/chat`

Request:
```json
{
  "message": "Update student 1 email to newemail@example.com"
}
```

Response: Updated student record in table format

### Delete Student
**POST** `/chat`

Request:
```json
{
  "message": "Delete student 1"
}
```

Response: Confirmation message with deleted student details

### Get Student Count
**POST** `/chat`

Request:
```json
{
  "message": "How many students do we have?"
}
```

Response: Total count of students in database

## Available Tools 🛠️

The chatbot has access to the following tools:

- **create_student**: Create a new student record
- **get_student**: Retrieve a specific student by ID
- **get_all_students**: Retrieve all student records
- **update_student**: Update existing student information
- **delete_student**: Delete a student record
- **get_students_count**: Get total number of students

## Example Usage 💡

```python
# Using Python requests library
import requests
import json

url = "http://localhost:5000/chat"

# Create a student
data = {
    "message": "Create a student named Ali Khan, 25 years old, BSSE department, ali@email.com"
}

response = requests.post(url, json=data)
print(response.json())
```

## Environment Variables 🔐

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | `xxxx-xxxx-xxxx` |
| `FLASK_DEBUG` | Enable/disable debug mode | `true` or `false` |
| `FLASK_ENV` | Flask environment | `development` or `production` |

## Database Schema 📊

### Student Model

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | Primary Key, Auto-increment |
| name | String(100) | Not Null |
| email | String(100) | Not Null, Unique |
| department | String(100) | Not Null |
| age | Integer | Not Null |

## Response Formatting 📋

All student management responses are formatted with:
- **Emojis**: Visual indicators (✅, ❌, 📋, 📊, ✏️, 🗑️)
- **Markdown Tables**: Clean table format for easy reading
- **Clear Messages**: User-friendly confirmation and error messages

## Troubleshooting 🔧

### ImportError: No module named 'groq'
```bash
pip install --upgrade langchain-groq
```

### Database is locked
Delete the `instance/` folder and reinitialize:
```bash
rm -rf instance/
python -c "from src import create_app; app = create_app(); [db.create_all() for _ in [app.app_context().push()]]"
```

### Groq API Key Error
Ensure your `.env` file contains a valid `GROQ_API_KEY` and the file is in the project root.

## Future Enhancements 🚀

- [ ] Add authentication/authorization
- [ ] Implement student grades tracking
- [ ] Add course enrollment management
- [ ] Batch student operations
- [ ] Advanced filtering and search
- [ ] Export student data (CSV, PDF)
- [ ] Student statistics and analytics dashboard
- [ ] Multi-language support

## Contributing 🤝

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License 📄

This project is open source and available under the MIT License.

## Author ✍️

Created for educational purposes to demonstrate Flask, LangChain, and AI integration.

## Support 💬

For questions or issues, please open an issue on the repository or contact the maintainer.

---

**Happy Learning!** 🎓
