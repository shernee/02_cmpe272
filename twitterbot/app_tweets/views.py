from multiprocessing.sharedctypes import Value
from django.http import HttpResponse
from django.shortcuts import render

from app_tweets import models, services

def home(request):    
    tweets = models.Tweet.objects.order_by('date_added')

    return render(request, 'tweets/home.html', {'tweets': tweets})

def posted(request):
    if request.method == "POST":
        tweet_text = request.POST.get("tweet")

        try:
            tweet_model = services.post_tweet(tweet_text=tweet_text)
        except ValueError:
            return HttpResponse("There is a problem with your request!")

        response_dict = {
            "id": tweet_model.tweet_id,
            "text": tweet_model.text
        }

        return render(
            request=request, 
            template_name='tweets/posted.html', 
            context=response_dict)


def deleted(request):

    tweet_id = request.POST.get("tweet-id")

    try:
        deleted_tweet_dict = services.delete_tweet(tweet_id=tweet_id)
    except ValueError:
        return HttpResponse("There is a problem with your request!")

    return render(
        request=request, 
        template_name='tweets/deleted.html', 
        context=deleted_tweet_dict)


def retrieved(request, tweet_id):

    try:
        tweet_model = services.retrieve_tweet(tweet_id=tweet_id)
    except ValueError:
        return HttpResponse("There is a problem with your request!")

    response_dict = {
        "id": tweet_model.tweet_id,
        "text": tweet_model.text,
        "create_at": tweet_model.date_added,
        "language": tweet_model.language,
        "author_id": tweet_model.author_id,
    }

    return render(request=request,
        template_name='tweets/retrieved.html', 
        context=response_dict)


