const fs = require('fs');
const stringSimilarity = require('string-similarity');

// Step 1: Load the fetched job data from the fetchedData.json file and CV resume
const fetchedData = JSON.parse(fs.readFileSync('./file/fetchedData.json', 'utf8'));
const cvData = JSON.parse(fs.readFileSync('./file/CV.json', 'utf8'));

// Step 2: Extract important fields from the CV
function extractResumeData(cv) {
    let skills = [];
    let roles = [];
    
  
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

    // Extract roles from CV's work experience
    if (cv.CompanyProfile && cv.CompanyProfile.employers) {
        cv.CompanyProfile.employers.forEach(emp => {
            emp.translations.forEach(translation => {
                roles.push(translation.title);
            });
        });
    }

    return { skills, roles };
}

// Step 3: Compare the resume with each job description
function compareCVWithJobs(cvData, fetchedData) {
    const cvResume = extractResumeData(cvData[0]); // Assume first CV for now

    const matchResults = fetchedData.map(job => {
        // Compare roles
        const roleMatch = stringSimilarity.compareTwoStrings(
            cvResume.roles.join(' '),
            job.roles.join(' ')
        );
        
        // Compare skills in CV with job description
        const skillMatch = stringSimilarity.compareTwoStrings(
            cvResume.skills.join(' '),
            job.description
        );
        
        
        const overallMatch = ((roleMatch + skillMatch) / 2) * 100;

        return {
            jobLink: job.link_to_assignment,
            roleMatch: (roleMatch * 100).toFixed(2) + '%',
            skillMatch: (skillMatch * 100).toFixed(2) + '%',
            overallMatch: overallMatch.toFixed(2) + '%'
        };
    });

    return matchResults;
}

// Step 4: Execute the matching process
const matchingResults = compareCVWithJobs(cvData, fetchedData);

// Output the results
console.log('Matching Results:', matchingResults);

// Save the results to a JSON file
fs.writeFileSync('matchingResults.json', JSON.stringify(matchingResults, null, 2), 'utf8');
console.log('Matching results saved to matchingResults.json');
