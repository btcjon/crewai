require('dotenv').config();
const axios = require('axios');

// Ensure the API key is trimmed to remove any extraneous whitespace
const apiKey = process.env.JSON2VIDEO_API_KEY.trim();
console.log(`Using API Key: '${apiKey}'`);  // Debug output to check the API key

const url = "https://api.json2video.com/v1/movie";

const data = {
    "comment": "10K 30 Days Blueprint Video",
    "resolution": "sd",
    "width": 360,
    "height": 640,
    "scenes": [
        {"duration": 5, "elements": [{"type": "image", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_In_a_sunlit_beachfront_villa_a_remarkably_accomplished_0.jpg"}]},
        {"duration": 5, "elements": [{"type": "image", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_strikingly_accomplished_young_woman_in_the_glamorous_0.jpg"}]},
        {"duration": 5, "elements": [{"type": "image", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_thriving_digital_marketer_embodying_success_and_yout_0.jpg"}]},
        {"duration": 5, "elements": [{"type": "image", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_thriving_digital_marketer_her_every_move_exudes_conf_0.jpg"}]},
        {"duration": 5, "elements": [{"type": "image", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_In_the_opulent_setting_of_a_chic_beachfront_villa_a_vi_0.jpg"}]},
        {"duration": 5, "elements": [{"type": "image", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_young_digital_marketer_excels_in_her_field_surrounde_0.jpg"}]},
        {"duration": 3, "elements": [{"type": "image", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_In_a_sumptuously_elegant_scene_we_see_a_prosperous_you_0.jpg"}]}
    ],
    "elements": [
        {"type": "audio", "src": "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/10K30DaysBlueprint.mp3", "start": 0, "duration": 33},
        {"type": "subtitles", "settings": {
            "style": "boxed-word", "font-family": "Luckiest Guy", "position": "bottom-center",
            "font-size": 200, "line-color": "#00FF00", "word-color": "#FFFF00",
            "max-words-per-line": 3, "outline-color": "#000000", "outline-width": 8
        }}
    ]
};

axios.post(url, data, {
    headers: {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json'
    }
})
.then(response => {
    console.log('Response:', response.data);
})
.catch(error => {
    console.log('Request Headers:', error.config.headers);
    console.error('Error:', error.response ? error.response.data : error.message);
});
