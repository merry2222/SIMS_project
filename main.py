# Programs Main execution

from skill_search.search import get_match
from job_fetch.get_data import fetch_data, get_descriptions
from employee_request.get_employee_skills import get_employee_skills
from grading.grade import grade

def calculate(all_scores):
    sum = 0
    for score in all_scores:
        sum+=score
    print(sum)
    return

# Kör fetch.js
fetch_data()
# Hämtar descriptions
descriptions = get_descriptions()
employees = get_employee_skills()

# Hittar matches (frågan om denna borde skrivas i ett snabbare språk)
for description in descriptions:
    # Här körs funktionen grade i grading/grade.py
    # TODO: Denna ska viktas med AI just nu räknar den bara upp
    grades = grade(description, get_match(description))
    for employee in employees:
        score = []
        for employee_skill in employee[1]:
            for graded_skill in grades:
                if employee_skill == graded_skill[0]:
                    score.append(graded_skill[1])
        calculate(score)