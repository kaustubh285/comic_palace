from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


def tweets_view(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
    }
    try:
        status = 200
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        status = 404
        data["message"] = "Invalid Value Entered"
    return JsonResponse(data, status=status)
    # return HttpResponse(f"<h1>Tweet is - {obj.content}</h1>")


def tweet_list_view(request, *args, **kwargs):
    obj = Tweet.objects.all()
    list_of_tweets = [{"id": x.id, "content": x.content} for x in obj]
    data = {
        "response": list_of_tweets
    }
    return JsonResponse(data, status=200)
