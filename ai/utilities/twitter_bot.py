import tweepy


class TwitterBot:
    def __init__(
        self,
        bearer_token: str,
        api_key: str,
        api_secret: str,
        access_token: str,
        access_token_secret: str,
    ):
        """Initialize Twitter bot with credentials"""
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def post_tweet(self, content: str) -> str:
        """
        Post a tweet

        Args:
            content (str): The content of the tweet

        Returns:
            str: Status message about the tweet
        """ """"""
        try:
            tweet = self.api.create_tweet(text=content)

            return f"Successfully posted tweet: {tweet.data}"
        except tweepy.TweepyException as e:
            print(f"{str(e)}")
            return f"Error posting tweet: {str(e)}"
