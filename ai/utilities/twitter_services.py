import os
from utilities.twitter_bot import TwitterBot
from dotenv import load_dotenv

load_dotenv()

# Twitter Creds Variable
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Twitter Bot
bot = TwitterBot(
    bearer_token=TWITTER_BEARER_TOKEN,
    api_key=TWITTER_API_KEY,
    api_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
)


# Test function to post listed NFT on Twitter => LET'S US THIS ONE FOR TESTING
def post_nft_on_twitter(nftName):
    """
    Market/Post NFT on X-Account

    Args:
        nftName (str):Name of the NFT that want to be posted/marketed

    Returns:
        str: Status message about the created post
    """
    try:

        return f"Successfully post/market NFT {nftName}"

    except Exception as e:
        return f"Error post NFT: {nftName}"


# Real Function to post on Twitter
def post_to_twitter(content: str):
    """
    Post a message to Twitter.

    Args:
        content (str): The content to tweet

    Returns:
        str: Status message about the tweet
    """
    return bot.post_tweet(content)
