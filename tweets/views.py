from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,Http404,JsonResponse, HttpResponseRedirect
from .models import Tweet
from django.shortcuts import render, redirect
import random
from .forms import TweetForm
from django.utils.http import is_safe_url
from django.views.decorators.csrf import csrf_protect
from .serializers import TweetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
# @csrf_protect
def home_view(requests,*args,**kwargs):
    # return HttpResponse("</h1>Hello World</h1>")
    print(requests.user or None)
    return render(requests,"pages/home.html",context={},status=200)

@api_view(['POST']) #http method from client should be POST
def tweet_create_view(requests,*args,**kwargs):
    print(requests.user)
    serializer =  TweetSerializer(data=requests.POST or None)
    if serializer.is_valid(raise_exception=True): #ths will send back what the error is
        serializer.save(user=requests.user)
        return Response(serializer.data,status=201)
    return Response({},status=400)


@api_view(['GET'])
def tweet_list_view(requests,*args,**kwargs):
    qs = Tweet.objects.all()
    serializer =  TweetSerializer(qs,many=True)
    return Response(serializer.data,status=200)



@api_view(['GET'])
def tweet_detail_view(requests,tweet_id,*args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj = qs.first()
    serializer =  TweetSerializer(obj)

    return Response(serializer.data,status=200)

# @csrf_protect
def tweet_create_view_pure_django(requests,*args,**kwargs):
    user = requests.user
    # print(kuchbhi)
    if not requests.user.is_authenticated:
        user = None
        if requests.is_ajax:
            return JsonResponse({},status=401) #401 -->> Not authorized
        return redirect(settings.LOGIN_URL) 
    print("Ajax request is:: {}".format(requests.is_ajax()))
    print("Requests is::: ",requests)
    form = TweetForm(requests.POST or None)
    print("Form is::: ",form)
    print("Request.POST is:: ",requests.POST)
    next_url = requests.POST.get("next") or None
    print("Next url is:: ",next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user #None would work if NULL=True is set in models (Annon User)
        #do other things as well    
        obj.save()
        if requests.is_ajax():
            return JsonResponse(obj.serialize(),status=201) #201 == typically for created items
        if next_url is not None and is_safe_url(next_url,allowed_hosts=ALLOWED_HOSTS):
            return redirect(next_url) #We want to make sure that the next url is a safe place to redirect to.
        form = TweetForm()
    if form.errors:
        if requests.is_ajax():
            return JsonResponse(form.errors,status=400)
    return render(requests,"components/forms.html",context={"form":form})

# @csrf_protect
def tweet_list_view_pure_django(requests,*args,**kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data ={
        "isUser":False,
        "response":tweets_list
    }
    return JsonResponse(data)

# @csrf_protect
def tweet_detail_view_pure_django(requests,tweet_id,*args,**kwargs):
    """
    REST API view
    Consume by JS or anything else
    
    """
    data = {
        "id":tweet_id,
        # 
    }
    status  = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data.update({"content":obj.content})
    except:
        data.update({"message":"Not found"})
        status= 404

    
    # return HttpResponse(f"</h1>Hello {tweet_id} - {obj.content}</h1>")
    return JsonResponse(data,status=status)

