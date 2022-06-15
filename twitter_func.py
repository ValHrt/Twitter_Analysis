import os
import tweepy
import statistics
import datetime
from PyQt5.QtWidgets import QMessageBox



class TwitterApiFunc:
    def __init__(self):
        super().__init__()
        # Authentification to Twitter API 
        self.auth = tweepy.OAuthHandler(os.environ.get("CONSUMER_KEY"),
                           os.environ.get("CONSUMER_SECRET"))
        self.auth.set_access_token(os.environ.get("TOKEN_KEY"),
                      os.environ.get("TOKEN_SECRET"))
        self.api = tweepy.API(self.auth)

    def comparison_infos(self, twitter_name: str, replies: bool, nb_tweets: int):
        # TODO : gérer les exceptions en cas de mauvais nom d'utilisateur
        try:
            user = self.api.get_user(screen_name=twitter_name)
            liste_likes = list()
            liste_retweets = list()
            most_fav_tweet = str()
            most_rt_tweet = str()
            tweets = tweepy.Cursor(self.api.user_timeline, screen_name=twitter_name,
                               tweet_mode="extended", include_rts=False,
                               exclude_replies=replies).items(nb_tweets)

            for tweet in tweets:
                #print(dir(tweet))
                liste_likes.append(tweet.favorite_count)
                liste_retweets.append(tweet.retweet_count)
                if tweet.favorite_count >= max(liste_likes):
                    most_fav_tweet = tweet.full_text
                if tweet.retweet_count >= max(liste_retweets):
                    most_rt_tweet = tweet.full_text

            return user.followers_count, max(liste_likes), max(liste_retweets),\
        int(statistics.mean(liste_likes)), int(statistics.mean(liste_retweets)),\
        round(statistics.mean(liste_likes)/user.followers_count*100, 2),\
        round(statistics.mean(liste_retweets)/user.followers_count*100, 2),\
        most_fav_tweet, most_rt_tweet, user.screen_name, user.profile_image_url

        except Exception as e:
            print(e)
            return (0, 0, 0, 0, 0, 0, 0, "?", "?", f"{twitter_name} pseudo not"
                    f" found ❌", "?")

    def get_tweets(self, keyword: str, nb_tweets: int, user_selected=None):
        if user_selected is None:
            query = f"-filter:retweets {keyword}"
        else:
            query = f"-filter:retweets {keyword} from:{user_selected}"

        try:
            tweets = tweepy.Cursor(self.api.search_tweets, q=query,
                                   tweet_mode="extended").items(nb_tweets)

            author_list = []
            tweet_list = []
            date_list = []
            like_list = []
            retweet_list = []

            for tweet in tweets:
                author_list.append(tweet.user.screen_name)
                tweet_list.append(tweet.full_text)
                date_list.append(tweet.created_at)
                like_list.append(tweet.favorite_count)
                retweet_list.append(tweet.retweet_count)

            date_list_cleaned = [date.strftime("%d-%m-%Y %H:%M:%S") for date in date_list]

            return author_list, tweet_list, date_list_cleaned, like_list, retweet_list

        except tweepy.errors.Forbidden:
            return "Keyword field cannot be empty"
