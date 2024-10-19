const fs = require('fs');
const stringSimilarity = require('string-similarity'); // calculate similarity b/w 2 strings

// Step 1: Load the fetched job data from the extracted_skills.json file and CV resume
const fetchedData = JSON.parse(fs.readFileSync('extracted_skills.json', 'utf8'));
const cvData = JSON.parse(fs.readFileSync('./files/CV.json', 'utf8'));

// Step 2: Extract important fields from the CV
function extractResumeData(cv) {
    let names = `${cv.User.firstName} ${cv.User.lastName}`;
    let id = cv.User.companyUserId;
    let skills = [];
  

    // Extract skills from CV
    if (cv.CompanyProfile && cv.CompanyProfile.workExperience) {
        cv.CompanyProfile.workExperience.forEach(exp => {
            if (exp.skills) {
                exp.skills.forEach(skill => {
                    skills.push(skill.keyword.masterSynonym);
                    skills = skills.concat(skill.keyword.synonyms);
                });
            }
        });
    }

    return { names, id, skills};
}

// Function to compare two strings using stringSimilarity with a threshold
function isSkillSimilar(skillFromCV, skillFromJob, threshold = 0.7) {
    const similarity = stringSimilarity.compareTwoStrings(skillFromCV.toLowerCase(), skillFromJob.toLowerCase());
    return similarity >= threshold;  // Match if similarity is above threshold
}

// Function to handle partial word matching for multi-word skills
function partialWordMatch(skillFromCV, skillFromJob) {
    const cvWords = skillFromCV.toLowerCase().split(' ');
    const jobWords = skillFromJob.toLowerCase().split(' ');
    
    // Check if any word in the CV skill matches any word in the job skill
    return cvWords.some(cvWord => jobWords.some(jobWord => isSkillSimilar(cvWord, jobWord)));
}

// Step 3: Compare the resume with each job description
function compareCVWithJobs(cvData, fetchedData) {
    const matchResults = cvData.map(cv => {
        const cvResume = extractResumeData(cv);

        const jobMatches = fetchedData.map(job => {
            let totalJobScore = 0;
            let matchedScore = 0;
            
            // Calculate total possible score from job extracted skills
            const jobSkills = job.extracted_skills || [];

            // Create a list of skill names from the CV for comparison
            const cvSkills = cvResume.skills.map(skill => skill.toLowerCase());

            jobSkills.forEach(jobSkill => {
                const skillName = jobSkill.skill_name.toLowerCase();
                const skillScore = jobSkill.score;

                // Add to total job score
                totalJobScore += skillScore;

                // If the skill from the job is similar to any CV skill or there is a partial word match
                const isMatched = cvSkills.some(cvSkill => 
                    isSkillSimilar(cvSkill, skillName) || partialWordMatch(cvSkill, skillName));
                
                if (isMatched) {
                    matchedScore += skillScore;
                }
            });

            // Calculate the percentage match score
            const matchPercentage = totalJobScore > 0 
                ? (matchedScore / totalJobScore) * 100 
                : 0;

            return {
                jobLink: job.job_link,
                roles: job.roles,
                skillMatch: matchPercentage.toFixed(2) + '%', // Return the match percentage
            };
        });

        return {
            userName: cvResume.names,
            userId: cvResume.id,
            matches: jobMatches
        };
    });

    return matchResults;
}

// Step 4: Execute the matching process
const matchingResults = compareCVWithJobs(cvData, fetchedData);

matchingResults.forEach(result => {
    console.log(`Candidate: ${result.userName}, ID: ${result.userId}`);
    result.matches.forEach((match, index) => {
        console.log(`  Job ${index + 1}:`);
        console.log(`    Job Link: ${match.jobLink}`);
        console.log(`    Skill Match: ${match.skillMatch}`);
        console.log(`    role:       ${match.roles}`);
    });
});

// Save the results to a JSON file
fs.writeFileSync('matchingResults.json', JSON.stringify(matchingResults, null, 2), 'utf8');
console.log('Matching results saved to matchingResults.json');
