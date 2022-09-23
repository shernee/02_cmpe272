from django.test import Client, TestCase
from unittest.mock import patch

from requests.models import Response

from app_tweets import services

TWEET_ID="123"
TWEET_TEXT="A Sample"

def create_mock_response(status_code: int, tweet_id: str, tweet_text: str) -> Response:
    resp = Response()
    resp.status_code = status_code
    response_string = f'{{"data": {{"id": "{tweet_id}", "text": "{tweet_text}"}}}}'
    
    resp._content = bytes(response_string, encoding='ascii')
    
    return resp


class PostedAPIServicesTest(TestCase):
    @patch('app_tweets.services.make_post_request')
    def test_bad_credentials(self, mock_make_post_request):
        """
        Test the creation of a Tweet object with a post request that returns 403
        """
        mock_make_post_request.return_value = create_mock_response(
            status_code=403, 
            tweet_id=TWEET_ID,
            tweet_text=TWEET_TEXT)

        with self.assertRaises(expected_exception=ValueError):
            services.post_tweet(tweet_text=TWEET_TEXT)


    @patch('app_tweets.services.make_post_request')
    def test_post_model(self, mock_make_post_request):
        """
        Test the creation of a Tweet object by checking if the tweet has been added to the database
        """
    
        mock_make_post_request.return_value = create_mock_response(
            status_code=201, 
            tweet_id=TWEET_ID,
            tweet_text=TWEET_TEXT)
      
        tweet_model = services.post_tweet(tweet_text=TWEET_TEXT)

        self.assertEqual(tweet_model.text, TWEET_TEXT)


class PostedViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('app_tweets.services.make_post_request')
    def test_details(self, mock_make_post_request):
        """
        Test the view on sending a post request to the POST api
        """
        
        mock_make_post_request.return_value = create_mock_response(
            status_code=201, 
            tweet_id=TWEET_ID,
            tweet_text=TWEET_TEXT)

        response = self.client.post('/tweets/posted/', data={"tweet": TWEET_TEXT})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, TWEET_ID)
        


    

