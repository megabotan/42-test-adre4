from django.test import TestCase
from django_hello_world.hello.models import Person, Request
from django.core.management import call_command
from django.conf import settings
from django.template import Template, Context


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
            self.assertTrue(Request.objects.filter(
                            path=expected_requests[i].path).exists())
        for i in range(reqests_on_page, reqests_on_page*2):
            self.assertNotContains(response, expected_requests[i].path)
            self.assertTrue(Request.objects.filter(
                            path=expected_requests[i].path).exists())

    def test_edit_page(self):
        new_name = self.me.name+'1'
        response = self.client.get('/edit/')
        self.assertRedirects(response, '/login/?next=/edit/')
        self.assertTrue(self.client.login(username='admin', password='admin'))
        photo = open('django_hello_world/hello/tests/test_image.jpg', 'r')
        response = self.client.post('/edit/',
                                    {'name': new_name,
                                     'last_name': self.me.last_name,
                                     'date_of_birth': self.me.date_of_birth,
                                     'bio': self.me.bio,
                                     'email': self.me.email,
                                     'jabber': self.me.jabber,
                                     'skype': self.me.skype,
                                     'other_contacts': self.me.other_contacts,
                                     'photo': photo,
                                     })
        response = self.client.get('/')
        self.assertContains(response, new_name)
        self.assertContains(response, 'Photo')

    def test_authorization_not_logined(self):
        response = self.client.get('/')
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Logout')

    def test_authorization_logined(self):
        self.client.login(username='admin', password='admin')
        response = self.client.get('/')
        self.assertNotContains(response, 'Login')
        self.assertContains(response, 'Logout')


class TemplateContextProcessorTest(TestCase):
    def test_settings(self):
        requestString = '/vblkzlcxvbru'
        response = self.client.get(requestString)
        self.assertTrue('settings' in response.context)
        self.assertEquals(response.context['settings'], settings)


class TemplateTagTest(TestCase):
    def setUp(self):
        self.me = Person.objects.get(id=settings.MY_ID)

    def test(self):
        template_str = '{% load custom_tags %}{% edit_link person %}'
        template = Template(template_str)
        context = Context({"person": self.me})
        self.assertEqual(template.render(context), '/admin/hello/person/1/')


class CommandTest(TestCase):
    def test_print_models(self):
        reqests_on_page = settings.REQUESTS_ON_PAGE
        for i in range(reqests_on_page):
            self.client.get('/')
        self.assertEquals(call_command('print_models'),
                          {'Persons': Person.objects.count(),
                           'Requests': Request.objects.count()})
