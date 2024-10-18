from google.oauth2 import service_account
import google.generativeai as genai
import re
# Funktion som körs för att vikta skills
def grade(description, matches):
    credentials = service_account.Credentials.from_service_account_file('grading/key.json') #API-key
    genai.configure(credentials=credentials)
    model = genai.GenerativeModel("gemini-1.5-flash-002") #Others models: "gemini-1.5-pro-002"
    skills_string = ", ".join([match[1] for match in matches]) #Skapar en sträng av alla matches
    prompt = f"""Given the following skills: [{skills_string}], and a job description below, evaluate each skill's relevance and importance in the context of the job description. For each skill, assign a grade between 0 and 3 based on how important the skill is in the job description.

        Skilldata is the name of the skill.
        Gradedata is a score between 0 and 3 where:
            0 = Useless not a skill or relevant to the job description or it's a job title
            1 = Merit
            2 = Should have
            3 = Must have

    Job Description: {description}

    Return the result only in this format for each skill:
    gradedata skilldata

    No additional explanations, commentary, or any other text should appear in the response—just the exact format with the grade and skill. Do not write out any empty posts, both skilldata and gradedata should contain something"""
    response = model.generate_content(prompt)
    print(response.text)
    grades = [] #Lista som håller alla grades av skills i formatet (skill:, score)
    for line in response.text.split('\n'):
        if line == '':
            continue
        words = line.split()
        skill = words[1]
        score = words[0]
        if score != '0' and skill: #Om score är 0 ignoreras det aka skräp-skills tex "Vi" resten kommer skickas vidare
            for match in matches:
                if match[1] == skill:
                    grades.append((match[0], score))
                    break
    if grades:
        return grades  # Returnerar grades format (skill_id, score)
    else:
        grade(description, matches) #Om inga grades hittas körs funktionen igen