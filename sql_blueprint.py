from flask import Blueprint, render_template, request

# Simulated user database with usernames, passwords, and bank balances
users = {
    "ponmuthu": {"password": "123456789", "balance": 5050},
}

# SQL Injection detection patterns
sql_injection_patterns = [
    "' OR '1'='1 --", "' OR 1=1 --", "1=1", "' OR 'x'='x", "--", "OR 1=1", "1=1 --"
]

# Define Blueprint
sql_app = Blueprint('sql_app', __name__)

@sql_app.route('/')
def home():
    return render_template('sql_index.html')

@sql_app.route('/sql_injection', methods=['POST'])
def sql_injection():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simulate query (for demonstration, do not use raw SQL in production)
    simulated_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    log_message = f"Simulated SQL Query: {simulated_query}"
    action_message = ""
    background_info = ""

    # SQL Injection detection: If any injection pattern is found in the password
    if any(pattern in password for pattern in sql_injection_patterns):
        # Simulate successful injection
        bank_balance = users["ponmuthu"]["balance"]
        action_message = f"SQL Injection Successful: You have bypassed the login! Your bank balance is ${bank_balance}."
        background_info = "SQL injection detected. The query was modified and bypassed the authentication."
        result = {
            "success": True,
            "message": action_message,
            "log": log_message,
            "background": background_info
        }
    elif username in users and users[username]["password"] == password:
        # Normal login: Check if username and password match
        bank_balance = users[username]["balance"]
        action_message = f"Login Successful! Your bank balance is ${bank_balance}."
        background_info = "Normal login attempt. Database query executed successfully."
        result = {
            "success": True,
            "message": action_message,
            "log": log_message,
            "background": background_info
        }
    else:
        # Invalid login: username or password incorrect
        result = {
            "success": False,
            "message": "Invalid username or password.",
            "log": log_message,
            "background": "Invalid login attempt. Database query failed."
        }

    return render_template('sql_result.html', result=result)
