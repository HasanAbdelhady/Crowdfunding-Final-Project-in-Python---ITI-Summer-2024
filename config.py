import json
from werkzeug.security import check_password_hash
from login_operations import *
class User_Operations:
    def __init__(self, file_path="login.json") -> None:
        self.file_path = file_path

    def save(self, first_name, last_name, email, password, phone_number):
        user_data = {}
        login_credentials = {"email": email, "password": password}
        user_info = {"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number}
        id = self.update_id()
        user_data[id] = {"login_credentials": login_credentials, "user_info": user_info, "user_projects":{}}

        try:
            with open(self.file_path, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}

        except FileNotFoundError:
            data = {}
            
        data.update(user_data)
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)


    def update_id(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                if not data:
                    return 0
                return max(int(key) for key in data.keys()) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
        
    def update_project_id(self,id,inner_key):
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                projects = data[id][inner_key]
                if projects == {}:
                    return str(0)
                return max(int(key) for key in data[id][inner_key].keys()) + 1
        except Exception as e:
            return e

    def verify_user(self, email):
        try:
            data = self.read_file()
            for user in data.values():
                if user["login_credentials"]["email"] == email:
                    return True
        except FileNotFoundError:
            return "No user data found"

    def read_file(self):
        with open(self.file_path, 'r') as file:
            read_file = json.load(file)
            return read_file
        
    def write_file(self, new_file):
        with open(self.file_path, 'w') as file:
            json.dump(new_file, file)

    def login(self, email, password):
            try:
                data = self.read_file()
                user_id = 0
                    
                for u_id, user in data.items():
                    if user["login_credentials"]["email"] == email and check_password_hash(user["login_credentials"]["password"],password):
                        user_id = u_id
                        print(self.user_dashboard(user["user_info"]["first_name"], user["user_info"]["last_name"]))
                        print("""Pick one of the Following Operations:
                                Create Project => 1
                                View All Projects => 2
                                Edit a Project => 3
                                Delete a Project => 4
                                Search for a Project using date => 5
                                """)
                        break
                    else:
                        print("Wrong Credentials")
                        exit()

                while True:
                    selection = int(input("Enter your selection: "))
                    if selection not in range(1,6):
                        raise ValueError("You can either enter 0 or 1")
                    
                    if selection == 1: #Create a new project
                        project = create_project()
                        project_id = self.update_project_id(user_id,"user_projects")
                        data[user_id]["user_projects"][project_id] = project

                        with open(self.file_path, 'w') as login_file:
                            json.dump(data, login_file)

                        print("Project Created Successfully")


                    elif selection == 2: #Show ALl Projcets
                        projects = data[user_id]["user_projects"]
                        if projects == {}:
                            print("You don't have any any projects yet")
                        else:
                            data = self.read_file()
                            projects = data[user_id]["user_projects"]
                            show_all_projects(projects)

                    elif selection == 3: #Edit Project
                        if data[user_id]["user_projects"] == {}:
                            print("You don't have any any projects yet to edit")
                        else:
                            show_all_projects(data[user_id]["user_projects"])
                            project_num = int(input("What project do you want to edit? (Numbers start from 1): ")) - 1
                            while True:
                                what_to_edit = int(input(f"""What do you want to edit?
                                                        1 => Title
                                                        2 => Details
                                                        3 => Target
                                                        4 => Start Date
                                                        5 => End Date """))
                                if what_to_edit not in range(6):
                                    raise ValueError("You can only pick a number from 1 to 5")
                                else:
                                    what_to_edit = edit_a_project(what_to_edit)
                                    break
                            edits_made = input("Enter your edit: ")
                            data[user_id]["user_projects"][str(project_num)][what_to_edit] = edits_made
                            data.update(data)
                            self.write_file(data)
                            print("Data Edited Successfully, these are your projects: ")
                            show_all_projects(data[user_id]["user_projects"])

                    elif selection == 4: #Delete a project
                        if data[user_id]["user_projects"] == {}:
                            print("You don't have any any projects yet to Delete")
                        else:
                            project_num = int(input("What project do you want to delete? (Numbers start from 1): ")) - 1
                            data[user_id]["user_projects"].pop(str(project_num))
                            self.write_file(data)
                            data = self.read_file()                
                            print("Project Deleted Successfully, these are your projects: ")
                            if data[user_id]["user_projects"] != {}:
                                show_all_projects(data[user_id]["user_projects"])
                        
                    elif selection == 5: #Select a Project using its start_date
                        if data[user_id]["user_projects"] == {}:
                            print("You don't have any any projects yet to fetch")
                        else:
                            date = input("Enter the date in DD/MM/YYYY format: ")
                            projects = data[user_id]["user_projects"]
                            for key in projects.keys():
                                if date == projects[key]["start_date"]:
                                    print(f"""
                                            Project Number: {key}
                                            Project Title: {projects[str(key)]["title"]}
                                            Project Details: {projects[str(key)]["details"]}
                                            Project Total Target: {projects[str(key)]["total_target"]}
                                            Project Start Date: {projects[str(key)]["start_date"]}
                                            Project Start Date: {projects[str(key)]["end_date"]} """)
                            
            except FileNotFoundError:
                return "No user data found"
            except ValueError as e:
                return e
    
    def user_dashboard(self,first_name, last_name):
        return f"Welcome to your Dashboard {first_name} {last_name}"
