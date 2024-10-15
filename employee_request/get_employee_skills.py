import json

def load_json():
    # Hard coded file
    file_path = 'employee_request/ut-anonymiserat-fmt.json'
    with open(file_path, 'r') as file:
        return json.load(file)


def get_employee_skills():
    employees = load_json()
    employee_skills = []
    
    for employee in employees:
        employee_id = employee['User']['id']
        all_skills = employee['CompanyProfile']['skills']
        work_skills = []
        for skill in all_skills:
            work_skills.append(skill['keyword']['id'])
        employee_skills.append((employee_id, work_skills))
    
    return employee_skills