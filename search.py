import json
import re

def load_skills_from_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def create_skill_regex(skill):
    return r'\b' + re.escape(skill) + r'\b'

# Makes a simple regex search and returns a 0 if no match, 1 if exact match or 2 if non exact
def get_match_scores(input_string, skills):
    matched_skills = []
    
    for skill in skills:
        master_synonym = skill['masterSynonym']
        all_synonyms = [master_synonym] + skill['synonyms']
        
        case_search = True
        matched_synonym = ""
        for synonym in all_synonyms:
            exact_match = re.search(create_skill_regex(synonym), input_string)
            if exact_match:
                case_search = False
                matched_synonym = synonym
                break
            
            if case_search:
                case_insensitive_match = re.search(create_skill_regex(synonym), input_string, re.IGNORECASE)
                if case_insensitive_match:
                    case_search = False
                    matched_synonym = synonym
        
        # Om skill över huvud taget finns appendas skillen
        if case_search == False:
            matched_skills.append((master_synonym, matched_synonym))
    
    return matched_skills

# Main execution
if __name__ == "__main__":
    json_file_path = 'alla_skills.json'  # Replace with your JSON file path
    skills = load_skills_from_json(json_file_path)
    
    input_string = """
    Uppdragsbeskrivning
    Vi söker en Senior C++ utvecklare på uppdrag av vår kund. Rollen innebär ett nära samarbete med teammedlemmar för att analysera projektkrav, designa och utveckla säker och effektiv kod samt underhålla den genom hela utvecklingscykeln. Du kommer att vara ansvarig för att identifiera och åtgärda prestandaflaskhalsar, felsöka och rätta till buggar samt säkerställa att kodbasen håller hög kvalitet. Dessutom kommer du att arbeta i en agil miljö och följa bästa praxis för att säkerställa en smidig och effektiv projektexekvering. Arbetet kommer att utföras på plats i vår kunds lokaler i Lund tre dagar i veckan.
    Obligatoriska kvalifikationer:
    Minst 5 års praktisk erfarenhet av C++-programmering.
    Expertis inom objektorienterad programmering, felsökning, algoritmer och prestandaoptimering.
    Erfarenhet av Test Driven Development, kontinuerlig integration och agila metoder.
    En kandidatexamen i mjukvaruutveckling eller ett relaterat område.
    Du måste behärska både svenska och engelska flytande, såväl i tal som i skrift.
    Det är meriterande om du har erfarenhet av Linux, SQL, Python, nätverksprotokoll, cybersäkerhet, Kubernetes och Docker.
    """
    
    matched_skills = get_match_scores(input_string, skills)
    
    print("\nDebug Information - Matched Skills:")
    for skill, matched_synonym in matched_skills:
        print(f"Skill: {skill}")
        print(f"Matched Synonym: {matched_synonym}")
        print("---")