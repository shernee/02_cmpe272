from dotenv import load_dotenv
import requests
import os
import json

load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")

tweet_fields = "tweet.fields=author_id,created_at,lang"

ids = "ids=1570441044277268483"

url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2ListLookupPython"
    return r

response = requests.request("GET", url, auth=bearer_oauth)

if(response.status_code != 200):
    raise Exception("Request returned an error: {} {}".format(response.status_code, response.text))

print("Response code: {}".format(response.status_code))

json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))

