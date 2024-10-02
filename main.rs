mod train_wordmap;
mod analyze;
use std::fs;
use serde_json::Value;
use std::error::Error;

fn main() {
    let files: [&str; 6] = ["src/data/c_sharp.json", "src/data/cpp.json", "src/data/java.json", "src/data/leader.json", "src/data/python.json", "src/data/security.json"];
    let names: [&str; 6] = ["C#", "C++", "Java", "Project-leader", "Python", "IT-Security"];
    let mut pattern: Vec<std::collections::HashMap<String, [f32; 3]>> = Vec::new();

    for job in files {
        let data = get_json(job).unwrap();
        let mut wordmap:std::collections::HashMap<String, [f32; 3]> = std::collections::HashMap::new();
        for description in data {
            train_wordmap::train_wordmap(&mut wordmap, description);
        }
        pattern.push(wordmap);
    }

    let target = get_json("src/target/currentData.json").unwrap();

    let mut j:i32 = 1;
    for job in target {
        println!("JOB NR: {:?}\n", j);
        j+=1;
        for i in 0..6 {
            println!("Match: {:?} , Job: {}\n", analyze::analyze(&pattern[i], 1.0, 1.0, 2.0, &job), names[i]);
        }
    }
}

fn get_json(file: &str) -> Result<Vec<String>, Box<dyn Error>> {
    //////////////////////////////////////////////////////
    // Snabbt snott hela JSON hämtningen från LLM
    let json_str = fs::read_to_string(file)?;
    let json: Value = serde_json::from_str(&json_str)?;

    let mut descriptions = Vec::new();

    if let Some(array) = json.as_array() {
        for item in array {
            if let Some(desc_array) = item["description"].as_array() {
                for desc in desc_array {
                    if let Some(desc_str) = desc.as_str() {
                        descriptions.push(desc_str.to_string());
                    }
                }
            }
        }
    }
    Ok(descriptions)
    //////////////////////////////////////////////////////
}