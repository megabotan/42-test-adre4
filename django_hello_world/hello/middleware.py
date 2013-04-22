from django_hello_world.hello.models import Request


class RequestMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated():
            request_user = request.user
            r = Request(path=request.path, method=request.method,
                        user=request_user)
        else:
            r = Request(path=request.path, method=request.method)
        r.save()
