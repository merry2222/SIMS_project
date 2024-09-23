//const fetch = require('node-fetch');
const fs = require('fs');

const url_1 = 'https://upgraded.se/wp-json/wp/v2/konsultuppdrag';
const url_2 = 'https://upgraded.se/wp-json/wp/v2/ort/';


fetch(url_1)
    .then(response => response.json())
    .then(data => {
        if (data.length > 0) {
            const ID = data[0].id;
            const new_url = `https://upgraded.se/wp-json/wp/v2/konsultuppdrag/${ID}`;
            console.log(`Fetching data from: ${new_url}`);

            return fetch(new_url);
        } else {
            console.log('No data found');
            return null;
        }
    })
    .then(response => {
        if (response) {
            return response.json();
        } else {
            return null;
        }
    })
    .then(newData => {
        if (newData) {
            const link_to_post = newData.link;
            const place = newData.ort[0];
            const roll_id = newData.roll[0];
            const description = newData.yoast_head_json.og_description;
            const url_3 = `${url_2}${place}`;
            console.log(`Fetching data from: ${url_3}`);

            return fetch(url_3).then(response => response.json()).then(placeData => {
                if (placeData) {
                    const result = {
                        link_to_post,
                        place: placeData.name,
                        roll_id,
                        description
                    };
                    writeToFile(result);
                } else {
                    console.log('No data found in place URL');
                }
            });
        } else {
            console.log('No data found in new URL');
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });

function writeToFile(data) {
    fs.writeFile('fetchedData.json', JSON.stringify(data, null, 2), (err) => {
        if (err) {
            console.error('Error writing to file:', err);
        } else {
            console.log('Data successfully written to fetchedData.json');
        }
    });
}