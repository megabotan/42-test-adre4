from django.shortcuts import render, get_object_or_404
from django_hello_world.hello.models import Person
from django.conf import settings


def home(request):
    person = get_object_or_404(Person, id=settings.MY_ID)
    return render(request, 'hello/index.html', {'person': person})
