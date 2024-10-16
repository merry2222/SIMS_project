from google.oauth2 import service_account
import google.generativeai as genai

# Funktion som körs för att vikta skills
def grade(description, matches):
    credentials = service_account.Credentials.from_service_account_file('key.json')
    genai.configure(credentials=credentials)
    model = genai.GenerativeModel("gemini-1.5-flash-002")
    # matches är en tuple (int(key), string(match found))
    grades = []
    i = 0
    for match in matches:
        # Returnerar Tuples med grades för varje skill
        grades.append((match[0], i))
        i+=1
    return grades