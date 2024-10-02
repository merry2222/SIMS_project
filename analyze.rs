mod split_into_array { include!("split_into_array.rs"); }
pub fn analyze(wordmap: & std::collections::HashMap<String, [f32; 3]>, x:f32, y:f32, z:f32, text: &String) -> f32 {
    let wordarray = split_into_array::split_into_array(text);
    // A correlation of 0 means the entire sentence is a perfect match
    let mut correlation: f32 = 0.0;
    // dc is the derivative of change (or the change of the change)
    let mut dc: f32 = 0.0;
    // Iterate through all sentences
    for (length, sentence) in wordarray.iter().enumerate() {
        // Iterate through all words
        for (height, word) in sentence.iter().enumerate() {
            // TODO: Maybe the entire calculation should be moved to a separate file????
            match wordmap.get(word) {
                Some(entry) => {
                    // TODO: It may be worth considering using ABS value here.
                    // As it stands now a mirrored text will give a lower value
                    // But maybe, this is what we want?
                    let c = entry[2]/((entry[0] / entry[2] - length as f32).abs() * x + (entry[1] / entry[2] - height as f32).abs() * y + 1 as f32);
                    // Why do we remove the change of change? We only want to know a single odd thing.
                    // Because, if we are off by one sentence, we do not want to calculate this twice, thrice or n times.
                    correlation += (c - dc).abs();
                    dc = c;
                }
                None =>
                    correlation -= z
            }
        }
    }
    return correlation;
}