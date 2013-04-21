from django_hello_world.hello.models import Person, Request
from django_hello_world.hello.forms import PersonForm
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
import os


def home(request):
    person = get_object_or_404(Person, id=settings.MY_ID)
    return render(request, 'hello/index.html', {'person': person})


def requests(request):
    first_requests = Request.objects.all().order_by('date')[:10]
    return render(request, 'hello/requests.html',
                  {'first_requests': first_requests})


@login_required
def edit(request):
    person = get_object_or_404(Person, id=settings.MY_ID)
    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        if form.is_valid():
            form = PersonForm(request.POST, request.FILES, instance=person)
            form.save()
            clear_images_folder(person.photo)
            response_data = {'result': 'Changes have been saved'}
            return HttpResponse(simplejson.dumps(response_data),
                                content_type="application/json")
        else:
            response_data = {'result': 'Error',
                             'errors': dict(form.errors.items())}
            return HttpResponse(simplejson.dumps(response_data),
                                content_type="application/json")
    else:
        form = PersonForm(instance=person)
    return render(request, 'hello/edit.html', {
        'form': form,
        'person': person
    })


def clear_images_folder(actual_photo):
    folder = os.path.join(os.path.dirname(__file__), 'static/media/images')
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if (os.path.isfile(file_path) and
           the_file != os.path.basename(actual_photo.path) and
           the_file != "default.jpg"):
            os.unlink(file_path)
