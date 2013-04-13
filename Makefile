MANAGE=python django_hello_world/manage.py
PYTHONPATH=`pwd`
DJANGO_SETTINGS_MODULE=django_hello_world.settings

test:
	$(MANAGE) test django_hello_world.hello.tests.regular_tests

selenium_test:
	$(MANAGE) test django_hello_world.hello.tests.selenium_tests

check_syntax:
	flake8 --exclude=migrations django_hello_world/hello

run:
	$(MANAGE) runserver

syncdb:
	$(MANAGE) syncdb --noinput  
	$(MANAGE) migrate
