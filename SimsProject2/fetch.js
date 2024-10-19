//const fetch = require('node-fetch');
const fs = require('fs');

const url_1 = 'https://upgraded.se/wp-json/wp/v2/konsultuppdrag?per_page=30';
const url_2 = 'https://upgraded.se/wp-json/wp/v2/ort/';
const url_role = 'https://upgraded.se/wp-json/wp/v2/roll/';


async function fetch_assignment() {
    try {
        const response = await fetch(url_1);
        const data = await response.json();
        const ids = data.map(item => item.id);
        const url_assigment = ids.map(id => `https://upgraded.se/wp-json/wp/v2/konsultuppdrag/${id}`);

        const results = [];


        for (const url of url_assigment) {
            const assignment_response = await fetch(url);
            const assignment_data = await assignment_response.json();
            const link_to_assignment = assignment_data.link;
            const role = assignment_data.roll;
            const place = assignment_data.ort;
            const description = assignment_data.yoast_head_json.og_description;

            let place_names = [];
            let role_names = [];

            if (Array.isArray(place)) {
                for (const placeId of place) {
                    const place_response = await fetch(`${url_2}${placeId}`);
                    const place_data = await place_response.json();
                    place_names.push(place_data.name);
                }
            } else {
                const place_response = await fetch(`${url_2}${place}`);
                const place_data = await place_response.json();
                place_names.push(place_data.name);
            }

            //console.log(`Role: ${role}, Places: ${place_names.join(', ')}`);

            if (Array.isArray(role)) {
                for (const roleId of role) {
                    const role_response = await fetch(`${url_role}${roleId}`);
                    const role_data = await role_response.json();
                    role_names.push(role_data.name);
                }
            } else {
                const role_response = await fetch(`${url_role}${roles}`);
                const role_data = await role_response.json();
                role_names.push(role_data.name);
            }

            results.push({
                link_to_assignment,
                roles: role_names,
                places: place_names,
                description
            });
            //console.log(`Roles: ${role_names.join(', ')}, Places: ${place_names.join(', ')}`);
        }
        fs.writeFile('fetchedData.json', JSON.stringify(results, null, 2), (err) => {
            if (err) throw err;
            console.log('Data written to file');
        });

    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

fetch_assignment();
