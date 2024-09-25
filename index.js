//const fetch = require('node-fetch');
const fs = require('fs');

// Takes embedded url instead so all data is fatched at the same time
const embedded_url = 'https://upgraded.se/wp-json/wp/v2/konsultuppdrag?_embed&per_page=100';


async function fetch_assignment() {
    try {
        // Same fetch
        const response = await fetch(embedded_url);
        const data = await response.json();

        // Immediatly maps link and description to 2 const
        const link_to_assignment = data.map(item => item.link);
        const description = data.map(item => [item.yoast_head_json.og_description]);

        // Then maps an array of all embedded "ort" names and "roll" names
        // Same map function
        const place_names = data.map(item => {
            // If item even exists (some items did not contain role names and that made the program crash)
            if (item._embedded["wp:term"][0]) {
                // Then return this item
                return item._embedded["wp:term"][0]
                    // Filter out the "ort" names
                    .filter(term => term.taxonomy === "ort")
                    // And map all results to an array
                    .map(term => term.name);
            }
            else return [];
        });

        // See prev for comments
        const role_names = data.map(item => {
            if (item._embedded["wp:term"][1]) {
                return item._embedded["wp:term"][1]
                    .filter(term => term.taxonomy === "roll")
                    .map(term => term.name);
            }
            else return [];
        });

        // Only loops through once and adds it to results
        const results = [];
        for (let i = 0; i < data.length; i++) {
            // Combines the 4 arrays to one array
            results.push({
                link_to_assignment: link_to_assignment[i],
                roles: role_names[i],
                places: place_names[i],
                description: description[i]
            });
        }

        // Writes to fetchedData.json
        fs.writeFile('fetchedData.json', JSON.stringify(results, null, 2), (err) => {
            if (err) throw err;
            console.log('Data written to file');
        });

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

fetch_assignment();
