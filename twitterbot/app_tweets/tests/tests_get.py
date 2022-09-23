from django.test import Client, TestCase
from unittest.mock import patch

from requests.models import Response

from app_tweets import models, services


TWEET_ID = "123"
TWEET_TEXT="A Sample"
CREATED_AT="2022-09-18T15:48:22.000Z"
LANGUAGE = "en"
AUTHOR_ID = "456"


def create_mock_response(status_code: int, 
                    tweet_id: str, 
                    tweet_text: str,
                    created_at: str,
                    language: str,
                    author_id: str) -> Response:
    resp = Response()
    resp.status_code = status_code
    response_string = f'{{"data": [{{"created_at": "{created_at}", "text": "{tweet_text}", "lang": "{language}", "id": "{tweet_id}", "author_id": "{author_id}"}}]}}'
    
    resp._content = bytes(response_string, encoding='ascii')
    
    return resp


class RetrievedAPIServicesTest(TestCase):
    def setUp(self):
        models.Tweet.objects.create(
            tweet_id=TWEET_ID, 
            text=TWEET_TEXT,
            date_added=CREATED_AT,
            language=LANGUAGE,
            author_id=AUTHOR_ID)

    @patch('app_tweets.services.make_get_request')
    def test_bad_credentials(self, mock_make_get_request):
 
        """
        Test the retrieval of a Tweet object with a get request that returns 403
        """

        mock_make_get_request.return_value = create_mock_response(
            status_code=403, 
            tweet_id=TWEET_ID,
            tweet_text=TWEET_TEXT,
            created_at=CREATED_AT,
            language=LANGUAGE,
            author_id=AUTHOR_ID)

        with self.assertRaises(expected_exception=ValueError):
            services.retrieve_tweet(tweet_id=TWEET_ID)


    @patch('app_tweets.services.make_get_request')
    def test_get_model(self, mock_make_get_request):
        """
        Test the retrieval of a Tweet object by checking if the right tweet has been retrieved from the database
        """
    
        mock_make_get_request.return_value = create_mock_response(
            status_code=200, 
            tweet_id=TWEET_ID,
            tweet_text=TWEET_TEXT,
            created_at=CREATED_AT,
            language=LANGUAGE,
            author_id=AUTHOR_ID)
      
        tweet_model = services.retrieve_tweet(tweet_id=TWEET_ID)

        self.assertEqual(tweet_model.text, TWEET_TEXT)


class RetrievedViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        models.Tweet.objects.create(
            tweet_id=TWEET_ID, 
            text=TWEET_TEXT,
            date_added=CREATED_AT,
            language=LANGUAGE,
            author_id=AUTHOR_ID)

    @patch('app_tweets.services.make_get_request')
    def test_details(self, mock_make_get_request):
        """
        Test the view on sending a get request to the GET api
        """
      
        mock_make_get_request.return_value = create_mock_response(
            status_code=200, 
            tweet_id=TWEET_ID,
            tweet_text=TWEET_TEXT,
            created_at=CREATED_AT,
            language=LANGUAGE,
            author_id=AUTHOR_ID)

        url = f'/tweets/retrieved/{TWEET_ID}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, TWEET_TEXT)
        


    

