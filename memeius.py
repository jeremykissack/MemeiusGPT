import openai
import os
import re
import requests
import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from dotenv import load_dotenv

from utils import SYSTEM_MESSAGE_MEME, SYSTEM_MESSAGE_SUMMARY, draw_text_with_border, generate_prompt, summarize_context
from instaBot import InstaPublisher
from redditCrawler import RedditBot

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key
openai.api_key = openai_api_key

# Create an instance of the RedditBot class
reddit_bot = RedditBot()

# Fetch the top post and comments
subreddit_name = 'technology'
time_filter = 'day'
comment_limit = 3
reddit_features = reddit_bot.get_top_post_and_comments(subreddit_name, time_filter, comment_limit)

# Summarize the reddit data using GPT-3.5-turbo
summary_messages = [
    {"role": "system", "content": SYSTEM_MESSAGE_SUMMARY},
    {"role": "user", "content": summarize_context(reddit_features)}
]

print(summary_messages)

gpt_summary_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=summary_messages
)
response_summary_text = gpt_summary_response['choices'][0]['message']['content']

print(gpt_summary_response)

# Generate a prompt for DALL·E 2 using GPT-3.5-turbo
messages = [
    {"role": "system", "content": SYSTEM_MESSAGE_MEME},
    {"role": "user", "content": generate_prompt(response_summary_text)}
]

print(messages)

gpt_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

print(gpt_response)

# Get the text
response_text = gpt_response['choices'][0]['message']['content']
meme_prompt = re.search(r"Meme Prompt:(.+?)\|", response_text).group(1).strip()
text = re.search(r"Text:(.+?)\|", response_text).group(1).strip().replace('"', "")
caption = re.search(r"Caption:(.+?)\|", response_text).group(1).strip().replace('"', "")
hashtags = re.search(r"Hashtags:(.+)", response_text).group(1).strip().replace('"', "")

# Check if any extracted value is empty
if not meme_prompt or not text or not caption or not hashtags:
    raise Exception("Some extracted values are empty. Terminating the script.")

print("Meme Prompt:", meme_prompt)
print("Text:", text)
print("Caption:", caption)
print("Hashtags:", hashtags)

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