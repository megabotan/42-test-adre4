from django.shortcuts import render, get_object_or_404
from django_hello_world.hello.models import Person, Request
from django.conf import settings


def home(request):
    person = get_object_or_404(Person, id=settings.MY_ID)
    return render(request, 'hello/index.html', {'person': person})


def requests(request):
    first_requests = Request.objects.all().order_by('date')[:10]
    return render(request, 'hello/requests.html',
                  {'first_requests': first_requests})
