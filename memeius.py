import openai
import os
import re
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv

from utils import SYSTEM_MESSAGE, draw_text_with_border, generate_prompt
from instaBot import InstaPublisher
from redditCrawler import RedditBot

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key
openai.api_key = openai_api_key

# Create an instance of the RedditBot class
reddit_bot = RedditBot()

# Fetch the top post and comments
subreddit_name = 'all'
time_filter = 'month'
comment_limit = 3
reddit_features = reddit_bot.get_top_post_and_comments(subreddit_name, time_filter, comment_limit)
print(reddit_features)

# Generate a prompt for DALL·E 2 using GPT-3.5-turbo
messages = [
    {"role": "system", "content": SYSTEM_MESSAGE},
    {"role": "user", "content": generate_prompt(reddit_features)}
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

# Extract the text
text_pattern = r"Text: (.*?) \| Caption:"
text_match = re.search(text_pattern, generated_text)

if text_match:
    text = text_match.group(1).replace('"', "").strip()
else:
    text = ""

# Extract the caption
caption_pattern = r"Caption: (.*?) \| Hashtags:"
caption_match = re.search(caption_pattern, generated_text)

if caption_match:
    caption = caption_match.group(1)
else:
    caption = ""

# Extract the hashtags
hashtag_pattern = r"(#[^\s]+)"
hashtag_match = re.findall(hashtag_pattern, generated_text)

hashtags = " ".join(hashtag_match)

print(hashtags)

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

# Use the extracted text variable for overlay
font = ImageFont.truetype("arial.ttf", 49)

# Wrap the text and calculate the position of the text
lines = textwrap.wrap(text, width=30)
textwidth, textheight = draw.textsize("\n".join(lines), font)
x = (img.width - textwidth) / 2
y = img.height - textheight - 100

# Overlay the text on the image
text_color = (255, 255, 255)  # White color
border_color = (0, 0, 0)  # Black color
border_thickness = 2

for line in lines:
    textwidth, textheight = draw.textsize(line, font)
    draw_text_with_border(
        draw,
        line,
        ((img.width - textwidth) / 2, y),
        font,
        text_color,
        border_color,
        border_thickness,
    )
    y += textheight

# Save the image with a sequential label
if not os.path.exists("memeHistory"):
    os.mkdir("memeHistory")

label = len(os.listdir("memeHistory")) + 1
filename = f"meme_{label}.jpg"
img.save(os.path.join("memeHistory", filename))
print("Saved image as:", filename)

# Check if the config folder exists and delete it
import shutil
config_folder = "config"
if os.path.exists(config_folder):
    shutil.rmtree(config_folder)

# Posting the Image to Instagram.
caption += f"\n\n{hashtags}"
print(caption)
insta = InstaPublisher()
insta.publish(img, caption)