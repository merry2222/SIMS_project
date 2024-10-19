# Programs Main execution
import subprocess
import json

from skill_search.search import get_match
from job_fetch.get_data import get_descriptions
from grading.grade import grade
from calculate_score import calculate_score

# Kör fetch.js
subprocess.run(['node', 'job_fetch/fetch.js'])

# Hämtar descriptions som JSON
result = subprocess.run(['node', 'employee_request/extract_data.js'], capture_output=True, text=True)


employee_data = json.loads(result.stdout)['results']

# Hämtar descriptions, link och role
descriptions = get_descriptions()

# Initialize an empty dictionary to store user data
user_data = {}

# Matches descriptions
for description in descriptions:
    grades = grade(description[2], get_match(description[2]))  # Grades is a list of tuples (skill_id, score, skill_name)
    for employee in employee_data:
        score = []
        miss = []
        employee_skills_set = set(employee['skills'])  # Convert employee skills to a set for faster lookup
        for graded_skill in grades:
            if graded_skill[0] in employee_skills_set:
                score.append(graded_skill[1])
            else:                                   # If the skill is not in the employee's skills, add it to the missed skills list
                if int(graded_skill[1]) >=2:        # Only add missed skills that are should have or must have
                    miss.append(graded_skill[2])

        # Create or update user entry
        if employee['id'] not in user_data:
            user_data[employee['id']] = {
                "UserID": employee['id'],
                "UserName": employee['name'],
                "Matches": []
            }

        # Add the match to the user's Matches list
        user_data[employee['id']]["Matches"].append({
            "Link": description[1],
            "Joblist": description[0],
            "SkillMatch": calculate_score(score, grades),
            "MissedSkills": miss
        })

# Convert the dictionary to a list for JSON serialization
output_data = list(user_data.values())

# Write the data to the JSON file
file_path = 'streamlit.json'
with open(file_path, 'w') as file:
    json.dump(output_data, file, indent=4)

print("Data saved to", file_path)
