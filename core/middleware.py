from django.http import HttpResponsePermanentRedirect


class LowercaseURLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if path.startswith('/static/') or path.startswith('/media/'):
            return self.get_response(request)
        if path != path.lower():
            new_path = path.lower()
            return HttpResponsePermanentRedirect(new_path + ('?' + request.META['QUERY_STRING'] if request.META.get('QUERY_STRING') else ''))
        return self.get_response(request)