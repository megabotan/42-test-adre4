from django.forms import ModelForm
from django_hello_world.hello.models import Person


class PersonForm(ModelForm):
    class Meta:
        model = Person
