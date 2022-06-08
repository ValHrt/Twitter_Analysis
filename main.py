import os
import tweepy
import statistics

# Authentification auprès de l'API Twitter

auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"),
                           os.environ.get("CONSUMER_SECRET"))

auth.set_access_token(os.environ.get("TOKEN_KEY"),
                      os.environ.get("TOKEN_SECRET"))

