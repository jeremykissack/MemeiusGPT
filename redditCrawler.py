import os
import praw
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Replace the following placeholders with your own credentials
client_id = os.getenv("REDDIT_ID")
client_secret = os.getenv("REDDIT_SECRET")
user_agent = os.getenv("REDDIT_AGENT")

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

def get_top_headlines_and_comments(subreddit_name, time_filter, post_limit, comment_limit):
    subreddit = reddit.subreddit(subreddit_name)
    top_posts = subreddit.top(time_filter=time_filter, limit=post_limit)
    
    for post in top_posts:
        print(f'Title: {post.title}\nURL: {post.url}\nScore: {post.score}\n')
        
        post.comments.replace_more(limit=0)
        top_comments = post.comments.list()[:comment_limit]
        
        for i, comment in enumerate(top_comments, start=1):
            print(f'Comment {i}:')
            print(comment.body)
            print('\n')
        print('-' * 80)

# Change 'all' to a specific subreddit name if you want top headlines from a specific subreddit.
subreddit_name = 'all'
time_filter = 'week' # 'day' for top headlines of the day
post_limit = 10 # Number of headlines to fetch
comment_limit = 3 # Number of top comments to fetch per post

get_top_headlines_and_comments(subreddit_name, time_filter, post_limit, comment_limit)
