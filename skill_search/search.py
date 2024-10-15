import json
import re

def load_json():
    # Hard coded file
    file_path = 'skill_search/alla_skills.json'
    with open(file_path, 'r') as file:
        return json.load(file)

def create_skill_regex(skill):
    return r'\b' + re.escape(skill) + r'\b'

# Makes a simple regex search and returns found skills
def get_match(job_description):
    skills = load_json()
    matched_skills = []
    
    for skill in skills:
        master_synonym = skill['id']
        all_synonyms = skill['synonyms']
        
        case_search = True
        matched_synonym = ""
        for synonym in all_synonyms:
            exact_match = re.search(create_skill_regex(synonym), job_description)
            if exact_match:
                case_search = False
                matched_synonym = synonym
                break
            
            if case_search:
                case_insensitive_match = re.search(create_skill_regex(synonym), job_description, re.IGNORECASE)
                if case_insensitive_match:
                    case_search = False
                    matched_synonym = synonym
        
        # Om skill över huvud taget finns appendas skillen
        if case_search == False:
            matched_skills.append((master_synonym, matched_synonym))
    
    return matched_skills