import os
import tweepy
from dotenv import load_dotenv
import time

load_dotenv(override=True)

# Twitter Creds Variable
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

client = tweepy.Client(
    bearer_token=TWITTER_BEARER_TOKEN,
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
)


# Test function to post listed NFT on Twitter => LET'S USE THIS ONE FOR TESTING
def post_nft_on_twitter(content:str):
    """
    Market/Post NFT on X-Account

    Args:
        content (str):Content about the NFT to post

    Returns:
        str: Status message about the created post
    """
    try:
        print(f"Posting NFT on Twitter...")
        tweet = client.create_tweet(text=content)
       
        print("Sleeping for 60 seconds before execute new cycle")
        time.sleep(60)
        
        return f"Successfully posted tweet: {tweet.data}"

    except tweepy.TweepyException as e:
        print(f"{str(e)}")
        return f"Error posting NFT on tweet: {str(e)}"

# Real Function to post on Twitter
def post_to_twitter(content: str):
    """
    Post a message to Twitter.

    Args:
        content (str): The content to tweet

    Returns:
        str: Status message about the tweet
    """
    try:

        tweet = client.create_tweet(text=content)
        return f"Successfully posted tweet: {tweet.data}"

    except tweepy.TweepyException as e:
        print(f"{str(e)}")
        return f"Error posting tweet: {str(e)}"
