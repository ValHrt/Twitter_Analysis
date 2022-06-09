import os
import tweepy
import statistics



class TwitterApiFunc:
    def __init__(self):
        super().__init__()
        # Authentification to Twitter API 
        self.auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"),
                           os.environ.get("CONSUMER_SECRET"))
        self.auth.set_access_token(os.environ.get("TOKEN_KEY"),
                      os.environ.get("TOKEN_SECRET"))
        self.api = tweepy.API(self.auth)

    def get_followers(self, twitter_name):
        user = self.api.get_user(screen_name=twitter_name)
        return user.followers_count
