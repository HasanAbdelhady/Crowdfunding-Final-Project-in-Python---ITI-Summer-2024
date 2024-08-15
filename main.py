import re
from werkzeug.security import check_password_hash, generate_password_hash
from config import User_Operations

#This project might need a Virtual Environment to run properly, if doesn't run normally, this is probably the issue
while True:
    try:
        op = User_Operations()
        mode = int(input("Welcome, if you're a new user enter 0, if you already have an account enter 1: "))
        if mode not in range(2):
            raise ValueError("You can either enter 0 or 1")
        if mode == 0:
            first_name = input("Enter Your First Name: ")
            last_name = input("Enter Your Last Name: ")
            while True:
                email = input("Enter Your Email: ")
                if re.search(r"@.*\.com$", email) is None:
                    print("Please enter a valid email")
                    continue
                if op.verify_user(email):
                    print("This email is already registered, Please use another email")
                else:
                    break
            password = generate_password_hash(input("Enter Your Password: "))
            while True:
                if check_password_hash(password, input("Confirm Your Password: ")):
                    break
            while True:
                phone_number = input("Enter Your Egyptian Phone Number: ")
                if re.search("^010|^011|^012|015", phone_number) is not None and len(phone_number) in range(10,12):
                    break
            op.save(first_name, last_name, email, password, phone_number)
            print("User Created Successfully, you can now login")
            break
        elif mode == 1:
            email = input("Enter Your Email: ")
            password = input("Enter Your Password: ")
            op.login(email, password)
            break

    except ValueError as v:
        print(v)
    except Exception as e:
        print(e)