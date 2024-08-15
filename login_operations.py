import re
def create_project():
    title = input("Enter the titel of your Campaign: ")
    details = input("Enter the details of your Campaign: ")
    total_target = input("Enter the total target of your Campaign: ")
    while True:
        start_date = input("Enter Start Time in format DD/MM/YYYY: ")
        if re.search(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$", start_date) is None:
            print("Please enter start time in the right format DD/MM/YYYY")
        else:
            break

    while True:
        end_date = input("Enter End Time in format DD/MM/YYYY: ")
        if re.search(r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$", end_date) is None:
            print("Please enter End time in the right format DD/MM/YYYY")
        else:
            break

    project = {"title":title, "details":details, "total_target":total_target, "start_date":start_date, "end_date":end_date}
    return project

def show_all_projects(projects):
    if projects == {}:
        print("You have no projects yet, create some")
    else:  
        for key in projects.keys():
            print(f"""
                    Project Number: {str(int(key) + 1)}
                    Project Title: {projects[str(key)]["title"]}
                    Project Details: {projects[str(key)]["details"]}
                    Project Total Target: {projects[str(key)]["total_target"]}
                    Project Start Date: {projects[str(key)]["start_date"]}
                    Project Start Date: {projects[str(key)]["end_date"]} """)

def edit_a_project(num):
    if num == 1:
        return "title"
    elif num == 2:
        return "details"
    elif num == 3:
        return "total_target"
    elif num == 4:
        return "start_date"
    elif num == 5:
        return "end_date"


