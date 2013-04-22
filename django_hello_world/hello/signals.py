from django.contrib.contenttypes.models import ContentType
from django_hello_world.hello.models import ObjectLog
from django.db.utils import DatabaseError


def signal(action_, sender, **kwargs):
    if sender.__name__ != 'ObjectLog':
        object_log = ObjectLog(
            model_type=ContentType.objects.get_for_model(sender),
            action=action_)
        try:
            object_log.save()
        except DatabaseError:
            pass


def init_signal(sender, **kwargs):
    signal('created', sender, **kwargs)


def edit_signal(sender, **kwargs):
    signal('edited', sender, **kwargs)


def delete_signal(sender, **kwargs):
    signal('deleted', sender, **kwargs)
