from google.oauth2 import service_account
import google.generativeai as genai
import re
# Funktion som körs för att vikta skills
def grade(description, matches):
    credentials = service_account.Credentials.from_service_account_file('grading/key.json') #API-key
    genai.configure(credentials=credentials)
    model = genai.GenerativeModel("gemini-1.5-flash-002") #Others models: "gemini-1.5-pro-002"
    skills_string = ", ".join([match[1] for match in matches]) #Skapar en sträng av alla matches
    prompt = f"From 0-3 to how important is the skill [{skills_string}] in this job description just give a score next to the skill(keyword) format should be score skill: " + description + "\n format should skill then score"
    response = model.generate_content(prompt)
    print(response.text)
    grades = [] #Lista som håller alla grades av skills i formatet (skill:, score)
    for line in response.text.split('\n'):
        match = re.match(r'(.+):\s*(\d+)', line)
        if match:
            skill = match.group(1).strip()
            score = int(match.group(2))
            if score != 0: #Om score är 0 ignoreras det aka skräp-skills tex "Vi" resten kommer skickas vidare
                for match in matches:
                    if match[1] == skill:
                        grades.append((match[0], score))
                        break
    return grades   #Returnerar grades format (skill_id, score)


""" #Testkod för att see om AI fungerar och ger ut rimliga värden
if __name__ == "__main__":
    description = "Vi söker en utvecklare som kan Java, vi vill att du kan Python"
    matches = [(5245, 'Utveclare'), (703, 'Java'), (11792, 'Vi'), (22070, 'Python')]
    print(grade(description, matches))
"""