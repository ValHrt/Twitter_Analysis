import os, csv
import tweepy
import statistics
import datetime
from PyQt5.QtWidgets import QMessageBox



class TwitterApiFunc:
    def __init__(self):
        # Authentification to Twitter API 
        try:
            with open(f"{os.getenv('HOME')}/.twi_auth/credentials.csv") as f:
                csv_reader = csv.reader(f)
                twi_credentials = next(csv_reader)
                f.close()

            try:
                self.auth = tweepy.OAuthHandler(twi_credentials[0], twi_credentials[1])
                self.auth.set_access_token(twi_credentials[2], twi_credentials[3])
                self.api = tweepy.API(self.auth)
                # To raise the error in the init method if credentials provided are
                # wrong
                if twi_credentials[4] == "Not tested" or twi_credentials[4] == "Invalid Login":
                    self.api.get_user(screen_name="elonmusk")
                    tmp_file = "tmp.csv"
                    with open(f"{os.getenv('HOME')}/.twi_auth/{tmp_file}", "w") as outFile:
                        writer = csv.writer(outFile)
                        twi_credentials = [twi_credentials[0], twi_credentials[1],
                                           twi_credentials[2], twi_credentials[3],
                                           "Valid Login"]
                        writer.writerow(twi_credentials)
                        os.rename(f"{os.getenv('HOME')}/.twi_auth/{tmp_file}",
                                  f"{os.getenv('HOME')}/.twi_auth/credentials.csv")
                        outFile.close()

                self.error_msg = "OK"

            except tweepy.errors.Unauthorized:
                self.error_msg = "Wrong Credentials"
                tmp_file = "tmp.csv"
                with open(f"{os.getenv('HOME')}/.twi_auth/{tmp_file}", "w") as outFile:
                    writer = csv.writer(outFile)
                    twi_credentials = [twi_credentials[0], twi_credentials[1],
                                       twi_credentials[2], twi_credentials[3],
                                       "Invalid Login"]
                    writer.writerow(twi_credentials)
                    os.rename(f"{os.getenv('HOME')}/.twi_auth/{tmp_file}",
                              f"{os.getenv('HOME')}/.twi_auth/credentials.csv")
                    outFile.close()

        except FileNotFoundError:
            self.error_msg = "Credentials Missing"

    def valid_connection(self, con_key: str, con_sec: str, tok_key: str,
                         tok_sec: str):
        try:
            self.auth_test = tweepy.OAuthHandler(con_key, con_sec)
            self.auth_test.set_access_token(tok_key, tok_sec)
            self.api_test = tweepy.API(self.auth_test)
            self.api_test.get_user(screen_name="elonmusk")
            return True
        except tweepy.errors.Unauthorized:
            return False

    def comparison_infos(self, twitter_name: str, replies: bool, nb_tweets: int):
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

    def get_tweets(self, keyword: str, nb_tweets: int, option_selected: str,
                   user_selected=None):
        if user_selected is None:
            query = f"-filter:retweets {keyword}"
        else:
            query = f"-filter:retweets {keyword} from:{user_selected}"

        try:
            if option_selected == "Recent":
                tweets = tweepy.Cursor(self.api.search_tweets, q=query,
                                   tweet_mode="extended").items(nb_tweets)
            else:
                tweets = tweepy.Cursor(self.api.search_tweets, q=query,
                                   tweet_mode="extended", result_type="popular").items(nb_tweets)

            tweet_id_list = []
            author_list = []
            tweet_list = []
            date_list = []
            like_list = []
            retweet_list = []

            for tweet in tweets:
                tweet_id_list.append(tweet.id)
                author_list.append(tweet.user.screen_name)
                tweet_list.append(tweet.full_text)
                date_list.append(tweet.created_at)
                like_list.append(tweet.favorite_count)
                retweet_list.append(tweet.retweet_count)

            date_list_cleaned = [date.strftime("%d-%m-%Y %H:%M:%S") for date in date_list]

            return tweet_id_list, author_list, tweet_list, date_list_cleaned, like_list, retweet_list

        except tweepy.errors.Forbidden:
            return "Keyword field cannot be empty"

    def simple_tweet(self, tweet_text: str, tweet_image: str):
        if tweet_image == "NoImg":
            self.api.update_status(status=tweet_text)
        else:
            media = self.api.media_upload(filename=tweet_image)
            self.api.update_status(status=tweet_text,
                                   media_ids=[media.media_id])

    def reply_tweet(self, tweet_id: str, tweet_text: str, tweet_image: str):
        if tweet_image == "NoImg":
            self.api.update_status(status=tweet_text,
                                   in_reply_to_status_id=tweet_id,
                                   auto_populate_reply_metadata=True)
        else:
            media = self.api.media_upload(filename=tweet_image)
            self.api.update_status(status=tweet_text,
                                   in_reply_to_status_id=tweet_id,
                                   auto_populate_reply_metadata=True,
                                   media_ids=[media.media_id])

    def bot_tweet(self, option_selected: str, keyword: str, nb_tweets: int,
                  tweet_text: str, tweet_image: str):
        dict_tweets = {}
        query = f"-filter:retweets {keyword}"

        if option_selected == "Tweet containing: ":
            tweets = tweepy.Cursor(self.api.search_tweets, q=query,
                                       tweet_mode="extended").items(nb_tweets)
        # Default to 50 to find tweet finishing with the right keyword
        elif option_selected == "Tweet finishing by: ":
            tweets = tweepy.Cursor(self.api.search_tweets, q=query,
                                   tweet_mode="extended").items(50)

        for tweet in tweets:
            dict_tweets[tweet.id] = tweet.full_text

        if option_selected == "Tweet finishing by: ":
            temp_dict = {}
            count = 0
            for key in dict_tweets:
                if count == nb_tweets:
                    break
                if dict_tweets[key].endswith(keyword) or\
                dict_tweets[key].endswith(f"{keyword} ?") or\
                dict_tweets[key].endswith(f"{keyword} !"):
                    count += 1
                    temp_dict[key] = dict_tweets[key]
            dict_tweets = temp_dict

        print(dict_tweets)

        if tweet_image == "NoImg":
            for key in dict_tweets:
                self.api.update_status(status=tweet_text,
                                       in_reply_to_status_id=key,
                                       auto_populate_reply_metadata=True)
        else:
            media = self.api.media_upload(filename=tweet_image)
            for key in dict_tweets:
                self.api.update_status(status=tweet_text,
                                       in_reply_to_status_id=key,
                                       auto_populate_reply_metadata=True,
                                       media_ids=[media.media_id])

        return len(dict_tweets)

    def get_trends_loc(self):
        return self.api.available_trends()

    def get_top_tweets(self, woeid_id: int, hashtags: bool):
        if hashtags:
            trends = self.api.get_place_trends(id=woeid_id)
        else:
            trends = self.api.get_place_trends(id=woeid_id, exclude="hashtags")
        #print(trends)
        trends_dict = {}
        if hashtags:
            for value in trends:
                for trend in value["trends"]:
                    if "#" in trend["name"]:
                        trends_dict[trend["name"]] = trend["tweet_volume"]
        else:
            for value in trends:
                for trend in value['trends']:
                    trends_dict[trend['name']] = trend["tweet_volume"]

        sorted_trends_dict = dict(sorted(trends_dict.items(), key=lambda item:
                                         item[1] or 0, reverse=True))
        #print(sorted_trends_dict)

        return sorted_trends_dict
