# MemeiusGPT

MemeiusGPT is an AI meme generator that creates unique and funny memes using OpenAI's GPT-3.5-turbo and DALL·E 2. The generated memes are then automatically posted to the Instagram page @MemeiusGPT.

## Features

- Generates meme ideas using OpenAI's GPT-3.5-turbo
- Creates meme images using OpenAI's DALL·E 2
- Automatically posts memes to the Instagram page @MemeiusGPT
- Saves generated memes in a local folder for archiving

## Dependencies

- Python 3.6+
- `openai` library
- `Pillow` library
- `requests` library
- `python-dotenv` library
- `textwrap` library

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/MemeiusGPT.git
   ```

2. Install the required libraries:

   ```
   pip install openai Pillow requests python-dotenv textwrap
   ```

3. Set up an environment file `.env` in the root directory with your OpenAI API key:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Set up the `InstaPublisher` class with your Instagram credentials (check the `instaBot.py` file for more details).

5. Run the script:

   ```
   python main.py
   ```

## How it Works

The script first generates a meme idea using GPT-3.5-turbo, which includes a meme prompt, meme text, caption, and relevant hashtags. The meme prompt is then sent to DALL·E 2 to generate an image. The meme text is overlaid on the generated image using the `Pillow` library.

The final meme image is saved in a local folder named `memeHistory` with a sequential label, and posted to the Instagram page @MemeiusGPT with the generated caption and hashtags.

## License

This project is licensed under the MIT License.
