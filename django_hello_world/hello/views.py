from django.contrib.auth.models import User
from django.shortcuts import render_to_response


def home(request):
    users = User.objects.filter()
    return render_to_response('hello/home.html',{'users': users})
