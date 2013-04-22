from django import forms
from django_hello_world.hello.models import Person


class CalendarWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('css/smoothness/jquery-ui-1.10.2.custom.css',)
        }
        js = ('js/jquery-1.9.1.js',
              'js/jquery-ui-1.10.2.custom.js',
              'js/my_widget.js',
              )


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        widgets = {
            'date_of_birth': CalendarWidget(),
        }
