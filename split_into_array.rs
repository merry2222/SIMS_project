pub fn split_into_array(text: &String) -> Vec<Vec<String>> {
    // Splits by sentences
    text.to_lowercase()
        .replace(",","")
        .split('.')
        .filter(|s| !s.trim().is_empty())
        // Iterates over every sentence and transforms them into a vec<String>
        .map(|sentence| {
            // For every sentence
            sentence
                // Split my whitespace
                .split_whitespace()
                // Transforms these into actual string objects
                .map(String::from)
                // Collects string objects as a Vec<String>
                .collect::<Vec<String>>()
        })
        // Collects all sentences as a Vec<Vec<String>> and returns this
        .collect()
}