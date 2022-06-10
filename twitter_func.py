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

    def comparison_infos(self, twitter_name: str, replies: bool, nb_tweets: int):
        # TODO : gérer les exceptions en cas de mauvais nom d'utilisateur
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
