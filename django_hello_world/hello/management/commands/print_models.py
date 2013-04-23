from django.core.management.base import BaseCommand
from django.db.models import get_models
import sys


def prepare_to_output(dictionary):
        result = ''
        for elem in dictionary:
            result += str(elem) + ' : ' + str(dictionary[elem]) + '\n'
        return result


class Command(BaseCommand):

    def handle(self, *args, **options):
        result = {}
        for model in get_models():
            result[model.__name__] = model.objects.count()
        output = prepare_to_output(result)
        for str_ in output.rstrip().split('\n'):
            sys.stderr.write('error: ' + str_ + '\n')
        return output
