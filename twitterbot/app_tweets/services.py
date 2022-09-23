from django.utils import dateparse

from requests_oauthlib import OAuth1Session
import logging
import requests
import os

from app_tweets import models
import errors


def get_oauth_session():
    consumer_key = os.environ.get("API_KEY")
    consumer_secret = os.environ.get("API_SECRET_KEY")
    access_token = os.environ.get("ACCESS_TOKEN")
    access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    oauth = OAuth1Session(client_key=consumer_key, 
        client_secret=consumer_secret, 
        resource_owner_key=access_token, 
        resource_owner_secret=access_token_secret)

    return oauth


def make_post_request(text: str):
    oauth = get_oauth_session()
    payload = { "text": text }
    url = "https://api.twitter.com/2/tweets"

    response = oauth.post(url, json=payload)

    return response

def make_delete_request(id: str):
    oauth = get_oauth_session()
    url = "https://api.twitter.com/2/tweets/{}".format(id)

    response = oauth.delete(url)

    return response


def make_get_request(id: str):
    bearer_token = os.environ.get("BEARER_TOKEN")
    tweet_fields = "tweet.fields=author_id,created_at,lang"
    ids = "ids={}".format(id)
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    headers = { "Authorization": f"Bearer {bearer_token}", "User-Agent": "v2ListLookupPython"}

    response = requests.request("GET", url, headers=headers)

    return response
    

def post_tweet(tweet_text):
    if len(tweet_text) < 1:
        raise ValueError("Minimum Tweet length not met")
    
    response = make_post_request(text=tweet_text)
    response_status = response.status_code

    if response_status == 201:
        posted_tweet_dict = response.json()["data"]
        tweet_model = models.Tweet.objects.create(tweet_id=posted_tweet_dict["id"], text=posted_tweet_dict["text"])
    else:
        logging.error("Request returned an error: {} {}".format(response_status, response.text))
        raise ValueError

    return tweet_model


def delete_tweet(tweet_id):
    try:
        tweet_model = models.Tweet.objects.get(tweet_id=tweet_id)
    except models.Tweet.DoesNotExist:
        logging.error(f'Tweet ID {tweet_id} does not exist')
        raise errors.TweetDoesNotExist

    response = make_delete_request(id=tweet_model.tweet_id)
    response_status = response.status_code

    if response_status == 200:
        tweet_model.delete()
    else:
        logging.error("Request returned an error: {} {}".format(response_status, response.text))
        raise ValueError

    return tweet_id


def retrieve_tweet(tweet_id):
    response = make_get_request(id=tweet_id)
    response_status = response.status_code

    if response_status == 200:
        retrieved_tweet = response.json()["data"][0]

        parsed_date = dateparse.parse_datetime(retrieved_tweet["created_at"])
        retrieved_tweet["created_at"] = parsed_date

        tweet_model = models.Tweet.objects.get(tweet_id=tweet_id)
        tweet_model.date_added = parsed_date
        tweet_model.language = retrieved_tweet["lang"]
        tweet_model.author_id = retrieved_tweet["author_id"]
        tweet_model.save()
    else:
        logging.error("Request returned an error: {} {}".format(response_status, response.text))
        raise ValueError

    return tweet_model



