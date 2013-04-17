from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models


class Command(BaseCommand):

    def handle(self, *args, **options):
        app = get_app('hello')
        result = {}
        for model in get_models(app):
            result[model._meta.verbose_name] = model.objects.count()
        return str(result) + '\n'
