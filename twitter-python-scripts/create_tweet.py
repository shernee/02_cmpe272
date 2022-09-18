from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session
import os
import json

load_dotenv()

consumer_key = os.environ.get("API_KEY")
consumer_secret = os.environ.get("API_SECRET_KEY")
payload = { 'text': "Hello, world! From Python.." }
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

url = "https://api.twitter.com/2/tweets"

oauth = OAuth1Session(client_key=consumer_key, 
    client_secret=consumer_secret, 
    resource_owner_key=access_token, 
    resource_owner_secret=access_token_secret)

response = oauth.post(url, json=payload)

if(response.status_code != 201):
    raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

print("Response code: {}".format(response.status_code))

json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))

