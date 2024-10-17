from google.oauth2 import service_account
import google.generativeai as genai
import re
# Funktion som körs för att vikta skills
def grade(description, matches):
    credentials = service_account.Credentials.from_service_account_file('grading/key.json') #API-key
    genai.configure(credentials=credentials)
    model = genai.GenerativeModel("gemini-1.5-flash-002") #Others models: "gemini-1.5-pro-002"
    skills_string = ", ".join([match[1] for match in matches]) #Skapar en sträng av alla matches
    prompt = f"From 0-3 to how important are the skills given: [{skills_string}]. Return the matches in the same format, ie. 1,2,3,0,2,1... Just give a score next to the skill(keyword) format should be score skill: " + description + "\n format should skill then score"
    response = model.generate_content(prompt)
    print(response.text)
    grades = [] #Lista som håller alla grades av skills i formatet (skill:, score)
    for line in response.text.split('\n'):
        if line == '':
            continue
        words = line.split()
        skill = words[1]
        score = words[0]
        if score != 0: #Om score är 0 ignoreras det aka skräp-skills tex "Vi" resten kommer skickas vidare
            for match in matches:
                if match[1] == skill:
                    grades.append((match[0], score))
                    break
    return grades   #Returnerar grades format (skill_id, score)