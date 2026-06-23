from django.http import HttpResponsePermanentRedirect


class LowercaseURLMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        if path != path.lower():

            url = path.lower()

            query_string = request.META.get("QUERY_STRING")

            if query_string:
                url += "?" + query_string

            return HttpResponsePermanentRedirect(url)

        response = self.get_response(request)

        return response