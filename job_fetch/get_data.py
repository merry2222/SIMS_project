
import json

def load_json():
    # Hard coded file
    file_path = 'job_fetch/fetched_data.json'
    with open(file_path, 'r') as file:
        return json.load(file)

# Makes a simple regex search and returns found skills
def get_descriptions():
    # TODO: Maybe fun fetch from here???
    data = load_json()
    descriptions = []
    
    for job in data:
        descriptions.append((job['roles'][0], job['link_to_assignment'], job['description']))

    return descriptions