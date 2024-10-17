

// Extract important fields from the CV
function extractResumeData() {
    // den senaste versionen 
    const fs = require('fs');

    // Step 1: Load the fetched job data from the fetchedData.json file and CV resume
    const cvData = JSON.parse(fs.readFileSync('./employee_request/ut-anonymiserat-fmt.json', 'utf8'));
    const names = cvData.map(item => `${item.User.firstName} ${item.User.lastName}`);
    const id = cvData.map(item => item.User.companyUserId);

    let skills = [];
    cvData.map(item => {
        let skillset = [];
        item.CompanyProfile.workExperience.forEach(exp => {
            if (exp.skills) {
                exp.skills.forEach(skill => {
                    let grab = true;
                    skillset.forEach(grabbed => {
                        if (grabbed == skill.keyword.id) { 
                            grab = false
                        }
                    })
                    if (grab) {
                        skillset.push(skill.keyword.id);
                    }
                });
            }
        })
        skills.push(skillset);
    });
    
    const results = [];
    for (let i = 0; i < id.length; i++) {
        // Combines the 4 arrays to one array
        results.push({
            id: id[i],
            name: names[i],
            skills: skills[i]
        });
    }

    return { results };
}

const result = extractResumeData();
console.log(JSON.stringify(result));