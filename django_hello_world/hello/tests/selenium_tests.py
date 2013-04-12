from django.test import LiveServerTestCase
from django.conf import settings


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
