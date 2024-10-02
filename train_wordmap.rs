mod split_into_array { include!("split_into_array.rs"); }

pub fn train_wordmap(wordmap: &mut std::collections::HashMap<String, [f32; 3]>, text: String) {
    let wordarray = split_into_array::split_into_array(&text);
    // Iterate through all sentences
    for (x, sentence) in wordarray.iter().enumerate() {
        // Iterate through all words
        for (y, word) in sentence.iter().enumerate() {
            // Check HashMap for word
            wordmap.entry(word.clone()).and_modify(|array|{
                // If entry exists add current x and y values
                array[0] += x as f32;
                array[1] += y as f32;
                array[2] += 1.0;
                // Otherwise add word as new entry
            }).or_insert([x as f32,y as f32, 1.0]);
        }
    }
    return;
}