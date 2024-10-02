
// den senaste versionen 
const fs = require('fs');
const stringSimilarity = require('string-similarity');

// Step 1: Load the fetched job data from the fetchedData.json file and CV resume
const fetchedData = JSON.parse(fs.readFileSync('./file/fetchedData.json', 'utf8'));
const cvData = JSON.parse(fs.readFileSync('./file/CV.json', 'utf8'));

// Step 2: Extract important fields from the CV
function extractResumeData(cv) {
    let names = `${cv.User.firstName} ${cv.User.lastName}`;
    let id = cv.User.companyUserId;
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

    return { names, id, skills, roles };
}

// Step 3: Compare the resume with each job description
function compareCVWithJobs(cvData, fetchedData) {
    const matchResults = cvData.map(cv => {
        const cvResume = extractResumeData(cv);
        
        const jobMatches = fetchedData.map(job => {
            // Convert roles and job description to strings safely
            const jobRoles = Array.isArray(job.roles) ? job.roles.join(' ') : '';
            const jobDescription = job.description ? job.description.toString() : '';
            const cvRoles = cvResume.roles.length > 0 ? cvResume.roles.join(' ') : '';
            const cvSkills = cvResume.skills.length > 0 ? cvResume.skills.join(' ') : '';

            // Compare roles
            const roleMatch = stringSimilarity.compareTwoStrings(
                cvRoles,
                jobRoles
            );
            
            // Compare skills in CV with job description
            const skillMatch = stringSimilarity.compareTwoStrings(
                cvSkills,
                jobDescription
            );

            const overallMatch = ((roleMatch + skillMatch) / 2) * 100;

            return {
                jobLink: job.link_to_assignment,
                roleMatch: (roleMatch * 100).toFixed(2) + '%',
                skillMatch: (skillMatch * 100).toFixed(2) + '%',
                overallMatch: overallMatch.toFixed(2) + '%'
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

// Output the results in a detailed format
matchingResults.forEach(result => {
    console.log(`Candidate: ${result.userName}, ID: ${result.userId}`);
    result.matches.forEach((match, index) => {
        console.log(`  Job ${index + 1}:`);
        console.log(`    Job Link: ${match.jobLink}`);
        console.log(`    Role Match: ${match.roleMatch}`);
        console.log(`    Skill Match: ${match.skillMatch}`);
        console.log(`    Overall Match: ${match.overallMatch}`);
    });
});

// Save the results to a JSON file
fs.writeFileSync('matchingResults.json', JSON.stringify(matchingResults, null, 2), 'utf8');
console.log('Matching results saved to matchingResults.json');
