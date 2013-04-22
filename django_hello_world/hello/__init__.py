from django_hello_world.hello import signals
from django.db.models.signals import post_init, post_save, post_delete
from django.db.models import get_app, get_models

app = get_app('hello')
for model in get_models(app):
    post_init.connect(signals.init_signal, sender=model)
    post_save.connect(signals.edit_signal, sender=model)
    post_delete.connect(signals.delete_signal, sender=model)
