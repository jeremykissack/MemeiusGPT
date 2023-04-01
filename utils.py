SYSTEM_MESSAGE = "You are a helpful assistant that generates long and creative meme prompts and short but funny texts."

def generate_prompt(reddit_features: dict) -> str:
    user_message = f"Generate a meme prompt and text for a really edgy meme based on the top Reddit post of the day. \
        Title: {reddit_features['title']}. Flair: {reddit_features['flair']}. Score: {reddit_features['score']}. Post text: {reddit_features['post_text']}. Top comments: {', '.join(reddit_features['top_comments'])}. \
        It should be low effort, but kinda stupid, and funny because it's stupid. \
        Dark humour is good, but it should not violate openAI's content policies. \
        Try to make the meme absolutely unhinged. \
        Also make a caption and around 20 hashtags for the post. \
        A meme prompt is used to generate the meme base image with DALL·E 2, \
            and the text part is intended to be overlaid on the image, completing the meme. \
        Use the format: 'Meme Prompt: [prompt] | Text: [text] | Caption: [caption] | Hashtags: [hashtags]'."

    return user_message


def draw_text_with_border(draw, text, position, font, text_color, border_color, border_thickness):
    x, y = position
    for i in range(-border_thickness, border_thickness + 1):
        for j in range(-border_thickness, border_thickness + 1):
            draw.text((x + i, y + j), text, font=font, fill=border_color)
    draw.text(position, text, font=font, fill=text_color)