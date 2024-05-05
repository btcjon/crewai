<?php
// Load dotenv library to handle environment variables (if needed)
// require 'vendor/autoload.php'; // Uncomment if using Composer
// $dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
// $dotenv->load();

// Manually set your API key here if not using dotenv
$apiKey = 'Your_JSON2Video_API_Key_Here'; // Replace with your API key

// API URL
$url = "https://api.json2video.com/v1/movie";

// Data array containing all parameters for the POST request
$data = [
    "comment" => "10K 30 Days Blueprint Video",
    "resolution" => "sd",
    "width" => 360,
    "height" => 640,
    "scenes" => [
        ["duration" => 5, "elements" => [["type" => "image", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_In_a_sunlit_beachfront_villa_a_remarkably_accomplished_0.jpg"]]],
        ["duration" => 5, "elements" => [["type" => "image", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_strikingly_accomplished_young_woman_in_the_glamorous_0.jpg"]]],
        ["duration" => 5, "elements" => [["type" => "image", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_thriving_digital_marketer_embodying_success_and_yout_0.jpg"]]],
        ["duration" => 5, "elements" => [["type" => "image", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_thriving_digital_marketer_her_every_move_exudes_conf_0.jpg"]]],
        ["duration" => 5, "elements" => [["type" => "image", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_In_the_opulent_setting_of_a_chic_beachfront_villa_a_vi_0.jpg"]]],
        ["duration" => 5, "elements" => [["type" => "image", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_A_young_digital_marketer_excels_in_her_field_surrounde_0.jpg"]]],
        ["duration" => 3, "elements" => [["type" => "image", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/Default_In_a_sumptuously_elegant_scene_we_see_a_prosperous_you_0.jpg"]]]
    ],
    "elements" => [
        ["type" => "audio", "src" => "https://cashdaily1.s3.amazonaws.com/10K30DaysBlueprint/10K30DaysBlueprint.mp3", "start" => 0, "duration" => 33],
        ["type" => "subtitles", "settings" => [
            "style" => "boxed-word", "font-family" => "Luckiest Guy", "position" => "bottom-center",
            "font-size" => 200, "line-color" => "#00FF00", "word-color" => "#FFFF00",
            "max-words-per-line" => 3, "outline-color" => "#000000", "outline-width" => 8
        ]]
    ]
];

$options = [
    "http" => [
        "method"  => "POST",
        "header"  => "Authorization: Bearer " . $apiKey . "\r\n" .
                     "Content-Type: application/json\r\n",
        "content" => json_encode($data),
        "ignore_errors" => true // Get content even on failure status
    ]
];

$context = stream_context_create($options);
$response = file_get_contents($url, false, $context);

if ($response === FALSE) {
    echo "Error making the request.\n";
} else {
    echo $response;
}
?>
