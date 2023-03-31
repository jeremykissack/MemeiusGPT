import openai
import os
import re
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key
openai.api_key = openai_api_key

# Generate a prompt for DALL·E 2 using GPT-3.5-turbo
messages = [
    {"role": "system", "content": "You are a helpful assistant that generates creative meme prompts and texts."},
    {"role": "user", "content": "Generate a meme prompt and text for a funny meme. Use the format: 'Meme Prompt: [prompt] | Text: [text]'."}
]

gpt_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

# Get the text
generated_text = gpt_response['choices'][0]['message']['content']
print(generated_text)

# Extract the meme prompt
meme_prompt_pattern = r"Meme Prompt: (.*?) \| Text:"
meme_prompt_match = re.search(meme_prompt_pattern, generated_text)

if meme_prompt_match:
    meme_prompt = meme_prompt_match.group(1)
else:
    meme_prompt = ""

# Generate an image using the DALL·E 2 API with the generated prompt
response = openai.Image.create(
    prompt=meme_prompt,
    n=1,
    size="1024x1024"
)


# Get the image URL
image_url = response['data'][0]['url']
print("Generated image URL:", image_url)

# Download the image from URL
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# Create a drawing context
draw = ImageDraw.Draw(img)

# Define the text to overlay
text = generated_text.split("|")[-1].strip()
font = ImageFont.truetype("arial.ttf", 36)

# Determine the size of the text
textwidth, textheight = draw.textsize(text, font)

# Calculate the position of the text
x = (img.width - textwidth) / 2
y = (img.height - textheight) / 2

# Overlay the text on the image
draw.text((x, y), text, font=font, fill=(255, 255, 255))

# Save the image
img.save('output.jpg')
