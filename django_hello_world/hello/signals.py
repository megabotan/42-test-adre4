from django.contrib.contenttypes.models import ContentType
from django_hello_world.hello.models import ObjectLog
from django.db.utils import DatabaseError
from django.dispatch import receiver
from django.db.models.signals import post_init, post_save, post_delete


def signal(action_, sender, instance, **kwargs):
    if sender.__name__ != 'ObjectLog' and sender.__name__ != 'ContentType':
        object_log = ObjectLog(
            model_type=ContentType.objects.get_for_model(sender),
            action=action_,
            object_id=instance.pk)
        try:
            object_log.save()
        except DatabaseError:
            pass


@receiver(post_init)
def init_signal(sender, instance, **kwargs):
    signal('created', sender, instance, **kwargs)


@receiver(post_save)
def edit_signal(sender, instance, **kwargs):
    signal('edited', sender, instance, **kwargs)


@receiver(post_delete)
def delete_signal(sender, instance, **kwargs):
    signal('deleted', sender, instance, **kwargs)
