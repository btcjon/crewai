import axios from 'axios';

const scenes = [
  "modern, luxurious home",
  "shopping",
  "yacht",
  "Private Jet Interior",
  "High-End Cafe",
  "Co-Working Space",
  "Beach"
];

const activities = [
  "Actively engaged in various digital marketing activities",
  "Managing Social Media",
  "Creating Content",
  "Creating “Live” video for social media"
];

const selectRandom = (options: string[]) => options[Math.floor(Math.random() * options.length)];

const generateImage = async () => {
  const scene = selectRandom(scenes);
  const activity = selectRandom(activities);
  const prompt = `Create a dynamic, very realistic image that captures the essence of a successful digital marketing lifestyle, tailored for women. The overall setting should be chic and high-tech, reflecting a sense of wealth and cutting-edge innovation. This vibrant and motivating atmosphere should ideally convey the lucrative potential of digital sales that guarantees significant earnings. Should depict a ${scene}. Feels both elegant and sophisticated with darker, moody lighting to enhance the atmosphere of exclusivity and success. Feature a young female entrepreneur ${activity}.`;

  const apiKey = process.env.OPENAI_API_KEY;
  const headers = {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  };
  const body = {
    prompt: prompt,
    n: 1,  // Number of images to generate
    size: "1024x1792"  // Size of the image
  };

  try {
    const response = await axios.post('https://api.openai.com/v1/images/generations', body, { headers });
    return response.data;
  } catch (error) {
    console.error('Error generating image:', error);
    return null;
  }
};

const generateMultipleImages = async (count: number) => {
  const results: any[] = [];  // Explicitly define the type of the array as any[]
  for (let i = 0; i < count; i++) {
    const imageData = await generateImage();
    results.push(imageData);
  }
  return results;
};

// Example webhook handler function
const handleWebhook = async (webhookData: any) => {
  const count = webhookData.body.count;  // Assuming 'count' is sent in the body of the POST request
  const images = await generateMultipleImages(count);
  return images;
};