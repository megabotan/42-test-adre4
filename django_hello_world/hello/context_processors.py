from django.conf import settings


def handle_settings(request):
    return {'settings': settings}
