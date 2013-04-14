from django import forms
from django_hello_world.hello.models import Person
from django.conf import settings


class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('/static/css/smoothness/jquery-ui-1.10.2.custom.css',)
        }
        js = (settings.STATIC_URL + 'js/jquery-1.9.1.js',
              settings.STATIC_URL + 'js/jquery-ui-1.10.2.custom.js',
              settings.STATIC_URL + 'js/my_widget.js',
              )


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        widgets = {
            'date_of_birth': CalendarWidget(),
        }
