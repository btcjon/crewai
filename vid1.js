require('dotenv').config();
const fs = require('fs');
const path = require('path');
const { Movie, Scene } = require("json2video-sdk");

async function main() {
    // Read and parse the assets.txt file
    const assetsPath = path.join(__dirname, '10K30DaysBlueprint/assets.txt');
    const assetsContent = fs.readFileSync(assetsPath, 'utf8');
    const lines = assetsContent.split('\n').map(line => line.trim());

    console.log(lines); // Log the lines to see what is being read from the file

    const mp3Url = lines.find(line => line.startsWith('MP3 URL')).split(': ')[1].trim();
    const totalLength = parseInt(lines.find(line => line.startsWith('Total Length')).split(': ')[1].split(' ')[0]);
    const totalScenes = parseInt(lines.find(line => line.startsWith('Total Scenes')).split(': ')[1]);

    let imageUrls = [];
    lines.forEach(line => {
        if (line.startsWith('S3 Image URL')) {
            let url = line.split(': ')[1].trim();
            if (url) {
                imageUrls.push(url);
            }
        }
    });

    console.log(imageUrls); // Log to check if URLs are complete and correct

    if (imageUrls.length === 0) {
        console.error("No valid image URLs found, aborting.");
        return;
    }

    let movie = new Movie({
        width: 720,
        height: 1280
    });

    movie.setAPIKey(process.env.JSON2VIDEO_API_KEY);

    // Define transitions
    const transitions = ["fade", "slide", "wipe", "fly"];

    // Calculate duration per scene
    const durationPerScene = totalLength / totalScenes;

    // Create scenes with one image each
    for (const source of imageUrls) {
        let scene = new Scene({
            duration: durationPerScene,
            transition: transitions[Math.floor(Math.random() * transitions.length)]
        });

        scene.addElement({
            type: "image",
            source: source,
            start: 0,
            duration: durationPerScene
        });

        movie.addScene(scene);
    }

    // Add an audio element to the movie
    movie.addElement({
        type: "audio",
        source: mp3Url,
        start: 0,
        duration: totalLength
    });

    // Render the movie
    try {
        let render = await movie.render();
        console.log("Rendering started. Project ID:", render.project);

        await movie.waitToFinish(status => {
            console.log("Rendering status:", status.movie.status, "/", status.movie.message);
        });
    } catch (err) {
        console.error("Error during rendering:", err);
    }
}

main();
