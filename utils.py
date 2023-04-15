from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

SYSTEM_MESSAGE_SUMMARY = "You are a information summarizer. You take in data relating to a social media post, and summarize it down to 3 to 5 concise bullet points."

def summarize_context(reddit_features: dict) -> str:
    analyzer = SentimentIntensityAnalyzer()
    
    title_sentiment = analyzer.polarity_scores(reddit_features['title'])
    post_text_sentiment = analyzer.polarity_scores(reddit_features['post_text'])
    top_comments_sentiments = [analyzer.polarity_scores(comment) for comment in reddit_features['top_comments']]
    
    user_message = f"This is a reddit post, comments, and its sentiment analysis. Summarize the following information in a few sentences: \
        Title: {reddit_features['title']}. Flair: {reddit_features['flair']}. Score: {reddit_features['score']}. Post text: {reddit_features['post_text']}. Top comments: {', '.join(reddit_features['top_comments'])}. \
        Title sentiment: {title_sentiment}. Post text sentiment: {post_text_sentiment}. Top comments sentiments: {top_comments_sentiments}. \
        "
    return user_message

SYSTEM_MESSAGE_MEME = "You are a helpful assistant that generates long and creative meme prompts and short but funny texts."


def generate_prompt(topic_summary) -> str:
    
    user_message = f"Generate a meme prompt and text for a really edgy meme based on the following information. \
        This is information relating to a reddit post, so pull details from this into the meme: {topic_summary}. \
        It should be low effort, but kinda stupid, and funny because it's stupid. \
        Dark humour is good, but it should not violate openAI's content policies. \
        Try to make the meme absolutely unhinged. \
        For the meme prompt, DO NOT INCLUDE ANYONES SPECIFIC NAME, rather, \
            describe the way they look instead if relevant. \
        Also make a caption and around 20 hashtags for the post. \
        A meme prompt is used to generate the meme base image with DALL·E 2, \
            and the text part is intended to be overlaid on the image, completing the meme. \
        Reiterating again, you CANNOT include the specific names of anyone in the meme prompt. \
        You must reply with the format: 'Meme Prompt: [prompt] | Text: [text] | Caption: [caption] | Hashtags: [hashtags]'."

    return user_message


def draw_text_with_border(draw, text, position, font, text_color, border_color, border_thickness):
    x, y = position
    for i in range(-border_thickness, border_thickness + 1):
        for j in range(-border_thickness, border_thickness + 1):
            draw.text((x + i, y + j), text, font=font, fill=border_color)
    draw.text(position, text, font=font, fill=text_color)