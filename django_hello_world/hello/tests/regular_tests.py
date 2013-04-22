from django.test import TestCase
from django_hello_world.hello.models import Person, Request, ObjectLog
from django_hello_world.hello.management.commands import print_models
from django_hello_world.hello.forms import CalendarWidget
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
        random_url = '/vblkzlcxvbru'
        for i in range(reqests_on_page*2):
            requestString = random_url + str(i)
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

    def test_requests_priority(self):
        reqests_on_page = settings.REQUESTS_ON_PAGE
        random_url = '/vblkzlcxvbru'
        for i in range(reqests_on_page*2):
            requestString = random_url + str(i)
            self.client.get(requestString)
        for i in range(reqests_on_page):
            obj = Request.objects.get(path='/vblkzlcxvbru'+str(i))
            obj.priority = 1
            obj.save()
        response = self.client.get('/requests/')
        expected_requests = (Request.objects.all()
                             .order_by('-priority')[:reqests_on_page*2]
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
        self.assertTrue(self.client.login(username='admin', password='admin'))
        response = self.client.get('/edit/')
        self.assertTrue(
            isinstance(response.context['form']['date_of_birth'].field.widget,
                       CalendarWidget))
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
        response = self.client.get('/edit/')
        self.assertRedirects(response, '/login/?next=/edit/')

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
        self.assertEquals(print_models.Command().handle().rstrip(),
                          'person : 1\nrequest : ' + str(reqests_on_page) +
                          '\nobject log : ' + str(ObjectLog.objects.count()))


class SignalTest(TestCase):
    def test_person(self):
        log_length = ObjectLog.objects.count()
        person = Person(name='name',
                        last_name='last_name',
                        date_of_birth='1999-01-01',
                        bio='bio',
                        email='email',
                        jabber='jabber',
                        skype='skype',
                        other_contacts='other_contacts'
                        )
        self.assertEquals(log_length + 1, ObjectLog.objects.count())
        last_change = ObjectLog.objects.latest('time')
        self.assertEquals(Person, last_change.model_type.model_class())
        self.assertEquals('created', last_change.action)
        person.name = 'name1'
        person.save()
        self.assertEquals(log_length + 2, ObjectLog.objects.count())
        last_change = ObjectLog.objects.latest('time')
        self.assertEquals(Person, last_change.model_type.model_class())
        self.assertEquals('edited', last_change.action)
        person.delete()
        self.assertEquals(log_length + 3, ObjectLog.objects.count())
        last_change = ObjectLog.objects.latest('time')
        self.assertEquals(Person, last_change.model_type.model_class())
        self.assertEquals('deleted', last_change.action)
