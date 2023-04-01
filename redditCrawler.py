# reddit_bot.py

import os
import praw
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()

class RedditBot:
    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")
        client_id = os.getenv("REDDIT_ID")
        client_secret = os.getenv("REDDIT_SECRET")
        user_agent = os.getenv("REDDIT_AGENT")

        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)

    def get_top_headlines_and_comments(self, subreddit_name: str, time_filter: str, post_limit: int, comment_limit: int):
        subreddit = self.reddit.subreddit(subreddit_name)
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

    def get_top_post_and_comments(self, subreddit_name: str, time_filter: str, comment_limit: int) -> Tuple[str, str, int, str, List[str]]:
        subreddit = self.reddit.subreddit(subreddit_name)
        top_post = next(subreddit.top(time_filter=time_filter, limit=1))

        title = top_post.title
        flair = top_post.link_flair_text or ''
        score = top_post.score
        post_text = top_post.selftext or ''

        top_post.comments.replace_more(limit=0)
        top_comments = [comment.body for comment in top_post.comments.list()[:comment_limit]]

        return {
            "title": title,
            "flair": flair,
            "score": score,
            "post_text": post_text,
            "top_comments": top_comments,
        }
