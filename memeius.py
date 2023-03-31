import openai
import os
import re
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv

from constants import SYSTEM_MESSAGE, PROMPT
from instaBot import InstaPublisher

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key
openai.api_key = openai_api_key

# Generate a prompt for DALL·E 2 using GPT-3.5-turbo
messages = [
    {"role": "system", "content": SYSTEM_MESSAGE},
    {"role": "user", "content": PROMPT}
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
text = generated_text.split("|")[-1].replace("Text:", "").replace('"', "").strip()
font = ImageFont.truetype("arial.ttf", 49)

# Wrap the text and calculate the position of the text
lines = textwrap.wrap(text, width=30)
textwidth, textheight = draw.textsize("\n".join(lines), font)
x = (img.width - textwidth) / 2
y = img.height - textheight - 100

# Overlay the text on the image
for line in lines:
    textwidth, textheight = draw.textsize(line, font)
    draw.text(((img.width - textwidth) / 2, y), line, font=font, fill=(255, 255, 255))
    y += textheight

# Save the image with a sequential label
if not os.path.exists("memeHistory"):
    os.mkdir("memeHistory")

label = len(os.listdir("memeHistory")) + 1
filename = f"meme_{label}.jpg"
img.save(os.path.join("memeHistory", filename))
print("Saved image as:", filename)

# Posting the Image to Instagram.

caption = """This is my first post ever  
#DeepFriedMemes #EdgyMemes #SurrealMemes #NihilistMemes #AntiMemes #MemeEconomy #MemeFormats #MemeTemplates #MemeGen #MemeWorld #MemeWar #MemeTherapy #MemeSquad #MemeMagic #MemeLords #MemeJunkie #MemeHeaven #MemeHell #MemeAddiction #MemeOverload"""
insta = InstaPublisher()
insta.publish(img, caption=caption)