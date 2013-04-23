from django_hello_world.hello.models import Person, Request, ObjectLog
from django.contrib import admin


class RequestAdmin(admin.ModelAdmin):
    list_display = ('path', 'method', 'user', 'date', 'priority')


class ObjectLogAdmin(admin.ModelAdmin):
    list_display = ('model_type', 'object_id', 'action', 'time')


admin.site.register(Person)
admin.site.register(Request, RequestAdmin)
admin.site.register(ObjectLog, ObjectLogAdmin)
