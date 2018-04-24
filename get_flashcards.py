# coding: utf-8

import tweepy 
import wget
import os
from settings import *

# consumer_key, consumer_secret, access_token and access_token_secret
# should be defined in settings.py file
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Get 200 of Chris' tweet
tweets = api.user_timeline(screen_name = 'chrisalbon', 
                           count = 200, 
                           include_rts = False, 
                           excludereplies = True)

# 200 isn't enough.  Keep getting tweets until we can't get anymore
last_id = tweets[-1].id
 
while (True):
    more_tweets = api.user_timeline(screen_name='chrisalbon',
                                count=200,
                                include_rts=False,
                                exclude_replies=True,
                                max_id=last_id-1)
                                    
    # There are no more tweets
    if (len(more_tweets) == 0):
          break
    else:
        last_id = more_tweets[-1].id-1
        tweets += more_tweets
        
# Chris stopped using a hashtag and started linking a URL
def has_ML_url(s):
    urls = s.entities.get('urls')
    if urls:
        return(urls[0].get('display_url') == 'machinelearningflashcards.com')
    else:
        return False

# Filter by those containing machinelearningflashcards.com
card_tweets = [tweet for tweet in tweets if has_ML_url(tweet)]

media_files = dict()
for status in card_tweets:
    title = status.text.split(' http')[0]
    media = status.entities.get('media', [])
    if(len(media) > 0 and media[0]['type']=='photo' ):  # if tweet has media and media is photo
        media_files[title] = media[0]['media_url']  # get me the url

os.makedirs('ml-flashcards', exist_ok=True) # make a directory to store the photos in

for text, url in media_files.items():
    wget.download(url, out = f'ml-flashcards/{text}.png') # get the photos!
