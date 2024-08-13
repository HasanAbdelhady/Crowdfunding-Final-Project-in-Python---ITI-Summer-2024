import json
from werkzeug.security import check_password_hash

def save(first_name, last_name, email, password, phone_number):
    user_data = {}
    login_credentials = {"email": email, "password": password}
    user_info = {"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number}
    id = update_id()
    user_data[id] = {"login_credentials": login_credentials, "user_info": user_info}

    try:
        with open("login.json", 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {}

    except FileNotFoundError:
        data = {}
        
    data.update(user_data)
    with open("login.json", 'w') as file:
        json.dump(data, file, indent=4)

def update_id():
    try:
        with open("login.json", 'r') as file:
            data = json.load(file)
            if not data:
                return 0
            return max(int(key) for key in data.keys()) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def verify_user(email):
    try:
        with open("login.json", 'r') as login_file:
            data = json.load(login_file)
            for user in data.values():
                if user["login_credentials"]["email"] == email:
                    return True
    except FileNotFoundError:
        return "No user data found"

def login(email, password):
    try:
        with open("login.json", 'r') as login_file:
            data = json.load(login_file)
            for user in data.values():
                if user["login_credentials"]["email"] == email and check_password_hash(user["login_credentials"]["password"],password):
                    return "Login successful"
                else:
                    continue
            return "Wrong Credentials"
    except FileNotFoundError:
        return "No user data found"
