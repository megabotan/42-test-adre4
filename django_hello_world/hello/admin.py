from django_hello_world.hello.models import Person, Request, ObjectLog
from django.contrib import admin

admin.site.register(Person)
admin.site.register(Request)
admin.site.register(ObjectLog)
