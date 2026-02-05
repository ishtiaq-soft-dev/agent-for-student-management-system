"""Utility functions for formatting responses in tabular format."""

def format_student_as_table(student_dict: dict) -> str:
    """Format a single student record as an HTML table."""
    html = """
    <table style="border-collapse: collapse; width: 100%; max-width: 600px; margin: 10px 0;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;"><strong>Field</strong></th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;"><strong>Value</strong></th>
        </tr>
    """
    
    for key, value in student_dict.items():
        html += f"""
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;"><strong>{key.capitalize()}</strong></td>
            <td style="border: 1px solid #ddd; padding: 8px;">{value}</td>
        </tr>
    """
    
    html += "    </table>\n"
    return html


def format_students_as_table(students_list: list) -> str:
    """Format multiple student records as an HTML table."""
    if not students_list:
        return "<p>No students found.</p>"
    
    html = """
    <table style="border-collapse: collapse; width: 100%; margin: 10px 0;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;"><strong>ID</strong></th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;"><strong>Name</strong></th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;"><strong>Email</strong></th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;"><strong>Department</strong></th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left;"><strong>Age</strong></th>
        </tr>
    """
    
    for student in students_list:
        html += f"""
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">{student.get('id', 'N/A')}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{student.get('name', 'N/A')}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{student.get('email', 'N/A')}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{student.get('department', 'N/A')}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">{student.get('age', 'N/A')}</td>
        </tr>
    """
    
    html += "    </table>\n"
    return html


def format_markdown_table(student_dict: dict) -> str:
    """Format a single student record as a markdown table."""
    markdown = "| Field | Value |\n|-------|-------|\n"
    
    for key, value in student_dict.items():
        markdown += f"| **{key.capitalize()}** | {value} |\n"
    
    return markdown


def format_markdown_table_multiple(students_list: list) -> str:
    """Format multiple student records as a markdown table."""
    if not students_list:
        return "No students found."
    
    markdown = "| ID | Name | Email | Department | Age |\n"
    markdown +="|----|------|-------|------------|-----|\n"
    
    for student in students_list:
        markdown += f"| {student.get('id', 'N/A')} | {student.get('name', 'N/A')} | {student.get('email', 'N/A')} | {student.get('department', 'N/A')} | {student.get('age', 'N/A')} |\n"
    
    return markdown
