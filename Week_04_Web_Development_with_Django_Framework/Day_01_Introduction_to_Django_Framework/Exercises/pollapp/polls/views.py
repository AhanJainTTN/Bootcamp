from django.http import HttpResponse


def say_hello(request):
    return HttpResponse("Hello! Welcome to Polls app.")
