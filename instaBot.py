import os
import tempfile
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
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            image.save(temp_file.name)
            
            # Upload the photo using the temporary file path
            self.bot.upload_photo(temp_file.name, caption=caption)
            
            # Clean up the temporary file
            os.remove(temp_file.name)
