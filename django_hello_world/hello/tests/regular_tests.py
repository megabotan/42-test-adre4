from django.test import TestCase
from django_hello_world.hello.models import Person
from django.conf import settings


class HttpTest(TestCase):
    def setUp(self):
        self.me = Person.objects.get(id=settings.MY_ID)

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, self.me.name)
        self.assertContains(response, self.me.last_name)
        self.assertContains(response,
                            self.me.date_of_birth.strftime('%B %d, %Y'))
        for string in self.me.bio.splitlines():
            self.assertContains(response, string)
        self.assertContains(response, self.me.email)
        self.assertContains(response, self.me.jabber)
        self.assertContains(response, self.me.skype)
        for string in self.me.other_contacts.splitlines():
            self.assertContains(response, string)
