const { Movie, Scene } = require("json2video-sdk");

async function main() {
    let movie = new Movie();

    // Set your API key
    movie.setAPIKey("Tijo1NM8RJ2c2QFyo4XS35N85dzuZXSL1yXui7Gd");

    // Create a new scene with a duration of 30 seconds
    let scene = new Scene({ duration: 30 });

    // Add an audio element
    scene.addElement({
        type: "audio",
        source: "https://yourdomain.com/path/to/your/voice.mp3",
        start: 0,
        duration: 30
    });

    // Add image elements
    const imageSources = [
        "https://yourdomain.com/path/to/image1.jpg",
        "https://yourdomain.com/path/to/image2.jpg",
        "https://yourdomain.com/path/to/image3.jpg",
        "https://yourdomain.com/path/to/image4.jpg",
        "https://yourdomain.com/path/to/image5.jpg",
        "https://yourdomain.com/path/to/image6.jpg"
    ];

    imageSources.forEach((source, index) => {
        scene.addElement({
            type: "image",
            source: source,
            start: index * 5,
            duration: 5
        });
    });

    // Add the scene to the movie
    movie.addScene(scene);

    // Render the movie
    let render = await movie.render();
    console.log("Rendering started. Project ID:", render.project);

    // Optionally, wait for the movie to finish rendering
    await movie.waitToFinish((status) => {
        console.log("Rendering: ", status.movie.status, " / ", status.movie.message);
    }).then((status) => {
        console.log("Movie is ready: ", status.movie.url);
    }).catch((err) => {
        console.log("Error: ", err);
    });
}

main();