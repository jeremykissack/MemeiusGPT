SYSTEM_MESSAGE = "You are a helpful assistant that generates long and creative meme prompts and short but funny texts."
PROMPT = "Generate a meme prompt and text for a really edgy meme (it should be low effort, but kinda stupid, and funny because it stupid), along with a caption and around 10 hashtags for the post. A meme prompt is used to generate the meme base image with DALL·E 2, and the text part is intended to be overlayed on the image, completing the meme. Use the format: 'Meme Prompt: [prompt] | Text: [text] | Caption: [caption] | Hashtags: [hashtags]'."

def draw_text_with_border(draw, text, position, font, text_color, border_color, border_thickness):
    x, y = position
    for i in range(-border_thickness, border_thickness + 1):
        for j in range(-border_thickness, border_thickness + 1):
            draw.text((x + i, y + j), text, font=font, fill=border_color)
    draw.text(position, text, font=font, fill=text_color)