from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from django.conf import settings
from django_hello_world.hello.models import Request


class HttpTestSelenium(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        from selenium.webdriver.firefox.webdriver import WebDriver
        cls.driver = WebDriver()
        super(HttpTestSelenium, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super(HttpTestSelenium, cls).tearDownClass()

    def test_check_admin_work_and_contains_Person(self):
        self.driver.get(self.live_server_url + '/admin/')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)  # checks admin is up
        username_field = self.driver.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.driver.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)  # checks you can login
        persons_links = self.driver.find_elements_by_link_text('Persons')
        self.assertEquals(len(persons_links), 1)  # checks Person in admin

    def test_requests_page(self):
        reqests_on_page = settings.REQUESTS_ON_PAGE
        for i in range(reqests_on_page*2):
            requestString = '/vblkzlcxvbru' + str(i)
            self.driver.get(self.live_server_url + requestString)
        self.driver.get(self.live_server_url + '/')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('requests', body.text)  # checks requests href
        self.driver.find_element_by_link_text('requests').click()
        body_text = self.driver.find_element_by_tag_name('body').text
        expected_requests = (Request.objects.all()
                             .order_by('date')[:reqests_on_page*2]
                             )
        for i in range(reqests_on_page):
            self.assertIn(expected_requests[i].path, body_text)
        for i in range(reqests_on_page, reqests_on_page*2):
            self.assertNotIn(expected_requests[i].path, body_text)

    def test_edit_page(self):
        self.driver.get(self.live_server_url + '/edit/')
        self.assertEquals(self.driver.current_url,
                          self.live_server_url + '/login/?next=/edit/'
                          )
        self.driver.get(self.live_server_url + '/')
        self.driver.find_element_by_link_text("Login").click()
        self.assertEquals(self.driver.current_url,
                          self.live_server_url + '/login/?next=/'
                          )
        username_field = self.driver.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.driver.find_element_by_name('password')
        password_field.send_keys('admin')
        password_field.send_keys(Keys.RETURN)
        self.assertEquals(self.driver.current_url,
                          self.live_server_url + '/'
                          )
        self.driver.find_element_by_link_text("Edit").click()
        self.assertEquals(self.driver.current_url,
                          self.live_server_url + '/edit/'
                          )
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Cancel', body.text)
        data = dict(name='name',
                    last_name='last_name',
                    bio='bio',
                    email='email@email.com',
                    jabber='jabber',
                    skype='skype',
                    other_contacts='other_contacts'
                    )
        for elem in data:
            field = self.driver.find_element_by_name(elem)
            field.clear()
            field.send_keys(data[elem])
        date_field = self.driver.find_element_by_name('date_of_birth')
        date_field.clear()
        date_field.send_keys("")
        self.driver.find_element_by_id("ui-datepicker-div")
        date_field.send_keys('01/01/1999')
        self.driver.find_element_by_name(data.keys()[0]).submit()
        self.driver.get(self.live_server_url + '/')
        body = self.driver.find_element_by_tag_name('body')
        for elem in data:
            self.assertIn(data[elem], body.text)
        self.assertIn('Jan. 1, 1999', body.text)
