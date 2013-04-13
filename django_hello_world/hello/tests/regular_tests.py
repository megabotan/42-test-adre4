from django.test import TestCase
from django_hello_world.hello.models import Person, Request
from django.conf import settings


class HttpTest(TestCase):
    def setUp(self):
        self.me = Person.objects.get(id=settings.MY_ID)

    def test_home(self):
        response = self.client.get('/')
        self.assertContains(response, self.me.name)
        for string in self.me.bio.splitlines():
            self.assertContains(response, string)

    def test_requests(self):
        reqests_on_page = settings.REQUESTS_ON_PAGE
        for i in range(reqests_on_page*2):
            requestString = '/vblkzlcxvbru' + str(i)
            self.client.get(requestString)
        response = self.client.get('/requests/')
        expected_requests = (Request.objects.all()
                             .order_by('date')[:reqests_on_page*2]
                             )
        for i in range(reqests_on_page):
            self.assertContains(response, expected_requests[i].path)
        for i in range(reqests_on_page, reqests_on_page*2):
            self.assertNotContains(response, expected_requests[i].path)


class TemplateContextProcessor(TestCase):
    def test_settings(self):
        requestString = '/vblkzlcxvbru'
        response = self.client.get(requestString)
        self.assertTrue('settings' in response.context)
        self.assertEquals(response.context['settings'], settings)
