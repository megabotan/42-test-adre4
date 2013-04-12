from django.test import TestCase
from django_hello_world.hello.models import Person
from django.conf import settings
from django.forms.models import model_to_dict


class HttpTest(TestCase):
    def setUp(self):
        self.me = Person.objects.get(id=settings.MY_ID)

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, self.me.name)
        for string in self.me.bio.splitlines():
            self.assertContains(response, string)
        my_info = model_to_dict(self.me)
        for field in my_info:
            self.assertContains(response, field)
