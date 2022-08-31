# Twitter Developer Toolbox

This application has been designed to use the Twitter API with a GUI.

![twitterapp](/readme_img/Twitter_App.png)

## Connection to the Twitter API

First of all, you need to put your credentials in the following windows. (*This window will appear the first time you use the app but you can accessing it later by clicking on the Authentification icon*) 

This module is used to save your twitter dev account credentials.

- **Important**: You need to have a developer account with **read and write access** to use all the functionalities of this application and avoid crash.
Your credentials are saved in .twi-auth directory inside your home directory. Please **don't remove it or modify it to avoid any issues**.

To apply to a twitter dev account you need to go on the [Twitter Developer portal](https://developer.twitter.com/en).

![authentificationmodule](/readme_img/Authentification_Module.png)

## Comparison module

This module allows you to compare two Twitter accounts to see who has the best statistics.
-To do this enter the two people to be compared.

-You can enter additional parameters, including the number of tweets to be considered (maximum 150) and wheter or not the search includes replies.

- **Issues**: It is possible that the search does not find a nickname that exists on Twitter. This is the case if the person has not tweeted enough (*e.g.: search on 50 tweets and the person has only tweeted 5 times*) or if he is in private mode.

- **Additional info**: It may take several seconds to run the search, especially if you are searching on a large number of tweets.

![comparisonmodule](/readme_img/Comparison_Module.png)

## Get Tweets module

This module allows you to search tweets by keyword, by user or both.

-There are several search options which are explained in the bottom right window.

- **Issues**: It is possible that the search does not return anything. Make sure you have unchecked the 'Select User' option if you have not entered a user name (*or check that the user name is correct*). If this option is unchecked but the search does not return anything, it means that no tweet in the last 30 days contains this keyword.

- **Information**: The searches for tweets are limited to the last 30 days by the Twitter API.

- **Search on user name only**: Enter a user's name without entering any keywords.

![gettweetsmodule](/readme_img/GetTweets_Module.png)

You can reply to a tweet by double clicking on it.

![gettweetsreply](/readme_img/GetTweets_Reply.png)

## Top Tweets module

This module allow you to get trending tweets from a selected location. You can choose trending tweets or trending hastags.

You can choose a country for the location, to do this, just select the country and then in the city list choose also the country name.

![toptweetsmodule](/readme_img/TopTweets_Module.png)

Double click on a trend will show you the top 10 tweets related to that trend. 

![top10tweets](/readme_img/Top10Tweets.png)

You can reply to a tweet by double clicking on it.

![toptweetsreply](/readme_img/TopTweets_Reply.png)

## Simple Tweet module

This module allow you to tweet from this application.

It will open a new window where you can enter your tweet and add an image if you want it to.

- **Issues**: If your tweet contains more than 280 characters you won't be able to post your tweet and get an error window.

![simpletweetmodule](/readme_img/SimpleTweetModule.png)

## Tweet Bot module

This module allow you to use a bot for reply to tweets that meet the criteria you have defined.

You can reply to tweets with text, image or both.

- **Issues**: If your tweet contains more than 280 characters you won't be able to post your tweet and get an error window.

![botmodule](/readme_img/Bot_Module.png)

### Compiling app

The app was compiled with PyInstaller.
