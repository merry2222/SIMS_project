# Programs Main execution
import subprocess
import json

from skill_search.search import get_match
from job_fetch.get_data import get_descriptions
from grading.grade import grade

def calculate(all_scores):
    sum = 0
    for score in all_scores:
        sum+=score
    return sum

def append_to_json(file_path, new_data):
    # Read existing data
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Append new data
    data.append(new_data)

    # Write updated data back to file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Kör fetch.js
subprocess.run(['node', 'job_fetch/fetch.js'])

# Hämtar descriptions som JSON
result = subprocess.run(['node', 'employee_request/extract_data.js'], capture_output=True, text=True)

# Laddar JSON
employee_data = json.loads(result.stdout)['results']

# Hämtar descriptions, link och role
descriptions = get_descriptions()

results = []

# Hittar matches (frågan om denna borde skrivas i ett snabbare språk)
for description in descriptions:
    # Här körs funktionen grade i grading/grade.py
    # TODO: Denna ska viktas med AI just nu räknar den bara upp
    grades = grade(description[2], get_match(description[2]))
    for employee in employee_data:
        score = []
        for employee_skill in employee['skills']:
            for graded_skill in grades:
                if employee_skill == graded_skill[0]:
                    score.append(graded_skill[1])
        total = calculate(score)

        # Example usage
        file_path = 'streamlit.json'
        new_user = {
            "UserID": employee['id'],
            "UserName": employee['name'],
            "Matches": {
                "Link": description[1],
                "Joblist": description[0],
                "SkillMatch": calculate(score)
            }
        }
        append_to_json(file_path, new_user)
        print("Data appended")