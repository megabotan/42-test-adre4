from django.core.management.base import BaseCommand
from django.db.models import get_app, get_models
import sys


def prepare_to_output(dictionary):
        result = ''
        for elem in dictionary:
            result += str(elem) + ' : ' + str(dictionary[elem]) + '\n'
        return result


class Command(BaseCommand):

    def handle(self, *args, **options):
        app = get_app('hello')
        result = {}
        for model in get_models(app):
            result[model._meta.verbose_name] = model.objects.count()
        output = prepare_to_output(result)
        sys.stderr.write("error:\n" + output)
        return output
