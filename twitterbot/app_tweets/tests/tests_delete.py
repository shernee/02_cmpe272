from django.test import Client, TestCase
from unittest.mock import patch

from requests.models import Response

from app_tweets import services, models

TWEET_ID="123"
TWEET_TEXT="A Sample"


def create_mock_response(status_code: int) -> Response:
    resp = Response()
    resp.status_code = status_code
    response_string = f'{{"data": {{"deleted": true}}}}'
    
    resp._content = bytes(response_string, encoding='ascii')
    
    return resp


class DeletedAPIServicesTest(TestCase):
    def setUp(self):
        models.Tweet.objects.create(tweet_id=TWEET_ID, text=TWEET_TEXT)

    @patch('app_tweets.services.make_delete_request')
    def test_bad_credentials(self, mock_make_delete_request):
        """
        Test the deletion of a Tweet object with a delete request that returns 403
        """
        mock_make_delete_request.return_value = create_mock_response(
            status_code=403)

        with self.assertRaises(expected_exception=ValueError):
            services.delete_tweet(tweet_id=TWEET_ID)


    @patch('app_tweets.services.make_delete_request')
    def test_delete_model(self, mock_make_delete_request):
        """
        Test the deletion of a Tweet object by checking if the tweet has been removed from the database
        """

        mock_make_delete_request.return_value = create_mock_response(
            status_code=200)

        before_count = models.Tweet.objects.count()     
        deleted_tweet_id = services.delete_tweet(tweet_id=TWEET_ID)
        after_count = models.Tweet.objects.count()

        self.assertEqual(deleted_tweet_id, TWEET_ID)

        self.assertEqual(after_count, before_count-1)

        with self.assertRaises(models.Tweet.DoesNotExist):
            models.Tweet.objects.get(tweet_id=TWEET_ID)


class DeletedViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        models.Tweet.objects.create(tweet_id=TWEET_ID, text=TWEET_TEXT)

    @patch('app_tweets.services.make_delete_request')
    def test_details(self, mock_make_delete_request):
        """
        Test the view on sending a post request to the DELETE api
        """
        
        mock_make_delete_request.return_value = \
            create_mock_response(status_code=200)

        response = self.client.post('/tweets/deleted/', data={"tweet-id": TWEET_ID})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, TWEET_ID)


        


    

