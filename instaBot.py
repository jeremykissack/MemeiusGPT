import os
from instabot import Bot
from dotenv import load_dotenv

load_dotenv()
USER = os.getenv("IG_USER")
PASS = os.getenv("IG_PASS")


class InstaPublisher:
    def __init__(self):
        self.bot = Bot()
        self.bot.login(username=USER, password=PASS)

    def publish(self, image, caption) -> None:
        self.bot.upload_photo(image, caption=caption)