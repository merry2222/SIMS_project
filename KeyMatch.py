# Example usage
#description = "This program searches one string for a bunch of keywords"
#keywords = ["python", "this", "This", "someone", "string"]

#result = KeyMatch(description, keywords)
#print(result)

def KeyMatch(description, keywords):
    description = description.lower()
    if [keyword.lower() in description for keyword in keywords]:
        return True
    else:
        return False
