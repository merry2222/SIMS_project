# Funktion som körs för att vikta skills
def grade(description, matches):
    # matches är en tuple (int(key), string(match found))
    grades = []
    i = 0
    for match in matches:
        # Returnerar Tuples med grades för varje skill
        grades.append((match[0], i))
        i+=1
    return grades