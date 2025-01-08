import re
import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Function to validate email format
def is_valid_email(email):
    valid_domains = [
        "@gmail.com", "@yahoo.com", "@outlook.com", "@hotmail.com", "@aol.com", "@icloud.com", "@mail.com",
        "@live.com", "@msn.com", "@protonmail.com", "@zoho.com", "@gmx.com", "@yandex.com", "@mail.ru"
    ]
    return any(email.endswith(domain) for domain in valid_domains)

# Function to validate phone number (should include country code)
def is_valid_phone_number(phone_number):
    phone_regex = r'^\+(\d{1,3})\s\d{7,12}$'
    return bool(re.match(phone_regex, phone_number))

# Function to check if email is recent (submitted within the last 24 hours)
def is_email_recent(email):
    connection = sqlite3.connect('enquiries.db')
    cursor = connection.cursor()
    cursor.execute('SELECT timestamp FROM enquiries WHERE email = ?', (email,))
    result = cursor.fetchone()
    connection.close()

    if result:
        last_submission_time = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
        if datetime.now() - last_submission_time < timedelta(hours=24):
            return True
    return False

# Endpoint to handle form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    message = data.get('message')

    errors = {}

    # Validation
    if not name or len(name) < 2:
        errors["name"] = "Name is required and must be at least 2 characters long."
    if not email or not is_valid_email(email):
        errors["email"] = "Invalid email format. Please use a valid email address like @gmail.com, @yahoo.com, etc."
    if not phone_number or not is_valid_phone_number(phone_number):
        errors["phone_number"] = "Phone number is invalid. It should include a country code and be between 7 and 12 digits long."
    if not message or len(message) < 5 or len(message) > 250:
        errors["message"] = "Message must be between 5 and 250 characters."
    if is_email_recent(email):
        errors["email_recent"] = "You cannot submit multiple enquiries within 24 hours using the same email."

    # If there are any validation errors, return them in the response
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    # Insert the form data into the SQLite database
    connection = sqlite3.connect('enquiries.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO enquiries (name, email, phone_number, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone_number, message))
    connection.commit()
    connection.close()

    return jsonify({
        "status": "success",
        "message": "Thank you for reaching out! We have received your enquiry and will get back to you shortly."
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
