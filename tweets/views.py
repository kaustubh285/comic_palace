import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetForm


ALLOWED_HOSTS = settings.ALLOWED_HOSTS


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


def tweet_form(request, *args, **kwargs):
    print(request.is_ajax())
    # Tweet form can be initialized with data or not
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    # If the form has data, it will first confirm if the form is valid
    if form.is_valid():
        obj = form.save(commit=False)
        # Can add other form related changes
        # Save to the db if  valid
        obj.save()
        if request.is_ajax():
            # Status 201 means Created Item
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            # is_safe_url will check if the url is of different hosts or if its safe.
            return redirect(next_url)
        # Reinitialize a blank form
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, "components/form.html", context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    obj = Tweet.objects.all()
    list_of_tweets = [x.serialize() for x in obj]
    data = {
        "isUser": False,
        "response": list_of_tweets
    }
    return JsonResponse(data, status=200)
