function assemble_url(params, find) {
    // Takes embedded url instead so all data is fatched at the same time
    var url = 'https://upgraded.se/wp-json/wp/v2/konsultuppdrag';

    // Assembles search keyword
    if (find) {
        params.push('search=' + find);
    }

    // Adds params
    first = true;
    for (const a of params) {
        if (first) {
            first = false;
            url += '?' + a;
            continue;
        }
        url += '&' + a;
    }
    return url;
}

async function fetch_data(url) {
    try {
        const response = await fetch(url);
        const responseJson = await response.json();
        return responseJson;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function write_to_file(filename, data_array) {
    //const fetch = require('node-fetch');
    const fs = require('fs');
    
    fs.writeFile(filename, JSON.stringify(data_array, null, 2), (err) => {
        if (err) throw err;
        //console.log('Data written to file');
    })
}

async function fetch_assignment(params, find, filelocation) {
    // Assembles URL
    const url = assemble_url(params, find);

    // Fetches data
    const data = await fetch_data(url);

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
            description: description[i][0]
        });
    }

    write_to_file(filelocation, results);
}


const testArgs = ['_embed', 'ort=154,26,656,25,593,106,98,151,24,120', 'per_page=100'];
const testSearch = '';
const testFile = 'job_fetch/fetched_data.json';

fetch_assignment(testArgs, testSearch, testFile);