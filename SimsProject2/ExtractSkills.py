import json
import spacy
from spacy.matcher import PhraseMatcher
from langdetect import detect
import re

# Load default skills database and import skill extractor
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor

# Load spaCy language models for English, Swedish, and Norwegian
nlp_en = spacy.load("en_core_web_lg")
nlp_sv = spacy.load("sv_core_news_lg")
nlp_no = spacy.load("nb_core_news_lg")

# Preprocess job descriptions by cleaning text
def preprocess_job_description(text):
    # Decode unicode escape sequences
    text = text.encode().decode('unicode_escape')
    
    # Remove punctuation
    clean_text = re.sub(r'[^\w\s]', '', text)
    
    # Replace multiple spaces with a single space
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    return clean_text.strip()

# Load custom skill database from 'alla_skills.json'
with open("./files/alla_skills.json", "r") as skill_file:
    custom_skills = json.load(skill_file)

# Function to add custom skills to SKILL_DB
def add_custom_skills_to_db(custom_skills, skill_db):
    for skill in custom_skills:
        master_synonym = skill["masterSynonym"].lower()
        synonyms = [syn.lower() for syn in skill["synonyms"]]
        skill_entry = {
            "skill_name": master_synonym,
            "skill_len": 1,
            "high_surfce_forms": {"full": master_synonym},
            "low_surface_forms": synonyms,
            "match_on_tokens": True
        }
        skill_db[master_synonym] = skill_entry

# Add custom skills from 'alla_skills.json' to SKILL_DB
add_custom_skills_to_db(custom_skills, SKILL_DB)

# Initialize skill extractors for each language
skill_extractor_en = SkillExtractor(nlp_en, SKILL_DB, PhraseMatcher)
skill_extractor_sv = SkillExtractor(nlp_sv, SKILL_DB, PhraseMatcher)
skill_extractor_no = SkillExtractor(nlp_no, SKILL_DB, PhraseMatcher)

# Custom stop words or irrelevant terms
custom_stop_words = set(['working with', 'using'])
custom_stop_words_no = set(['er', 'samt', 'person', 'av', 'på', 'med', 'i', 'en', 'et', 'som'])

# Function to remove stop words and irrelevant phrases
def filter_stop_words(skill_name, lang):
    if skill_name.lower() in custom_stop_words:
        return False
    if lang == 'sv' and skill_name.lower() in nlp_sv.Defaults.stop_words:
        return False
    elif lang == 'no' and (skill_name.lower() in nlp_no.Defaults.stop_words or skill_name.lower() in custom_stop_words_no):
        return False
    elif skill_name.lower() in nlp_en.Defaults.stop_words:
        return False
    elif lang == 'en' and skill_name.lower() in nlp_en.Defaults.stop_words:
        return False
    return True

# Loop through job descriptions and extract skills with ranking based on score
def extract_skills_from_job_descriptions(job_descriptions):
    extracted_skills_list = []
    for job in job_descriptions:
        job_description = job.get("description", "").strip()
        roles = job.get("roles", [])

        # Preprocess the job description
        job_description = preprocess_job_description(job_description)

        # Detect language
        try:
            lang = detect(job_description)
            
            # Skip if the job description is in Norwegian
            if lang == 'nb':  # 'nb' for Norwegian Bokmål
                print(f"Job description is in Norwegian. Skipping job {job['link_to_assignment']}.")
                continue
            
        except Exception as e:
            print(f"Error detecting language for job {job['link_to_assignment']}: {e}")
            continue

        # annotates the text, meaning it identifies parts of the text,
        # that match skills from the database and assigns labels to them
        try:
            if lang == 'sv':
                annotations = skill_extractor_sv.annotate(job_description)
            elif lang == 'en':
                annotations = skill_extractor_en.annotate(job_description)
            else:
                print(f"Unsupported language '{lang}' for job {job['link_to_assignment']}")
                continue
        except IndexError as e:
            print(f"Error processing job {job['link_to_assignment']}: {e}")
            continue

        # Extract skills with ranks from 'full_matches' and 'ngram_scored'
        extracted_skills = []
        if "full_matches" in annotations["results"]:
            for match in annotations["results"]["full_matches"]:
                skill_name = match["doc_node_value"].lower()
                if filter_stop_words(skill_name, lang):
                    score = float(match.get("score", 0))  # Use score as rank
                    extracted_skills.append({
                        "skill_name": skill_name,
                        "score": score  # Keep score as rank/importance
                    })

        if "ngram_scored" in annotations["results"]:
            for match in annotations["results"]["ngram_scored"]:
                skill_name = match["doc_node_value"].lower()
                if filter_stop_words(skill_name, lang):
                    score = float(match.get("score", 0))  # Use score as rank
                    extracted_skills.append({
                        "skill_name": skill_name,
                        "score": score  # Keep score as rank/importance
                    })

        # Post-process skills to remove duplicates (keep the highest score for duplicates)
        unique_skills = {}
        for skill in extracted_skills:
            skill_name = skill["skill_name"]
            if skill_name not in unique_skills or skill["score"] > unique_skills[skill_name]["score"]:
                unique_skills[skill_name] = skill
        
        consolidated_skills = list(unique_skills.values())

        # Add the job link, job description, and extracted skills
        extracted_skills_list.append({
            "job_link": job["link_to_assignment"],
            "job_description": job_description,
            "roles": roles,
            "extracted_skills": consolidated_skills
        })

    return extracted_skills_list

# Example usage
with open("fetchedData.json", "r") as json_file:
    fetched_data = json.load(json_file)

extracted_skills_list = extract_skills_from_job_descriptions(fetched_data)

# Save the extracted skills to a JSON file, including the job description
with open("extracted_skills.json", "w") as output_file:
    json.dump(extracted_skills_list, output_file, indent=4)

print("Skills have been extracted and saved.")