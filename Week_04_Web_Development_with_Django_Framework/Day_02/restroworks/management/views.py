from django.http import HttpResponse
from django.shortcuts import render


from .models import Customer, Order, MenuItem


def who_am_i(request):
    return HttpResponse(request.user)


def get_all_customers(request):
    response = (
        HttpResponse(Customer.objects.all())
        if request.user.is_superuser
        else HttpResponse("Unauthorised", status=403)
    )

    return response


def get_customer(request, name):
    response = (
        HttpResponse(Customer.objects.get(first_name=name))
        if request.user.is_superuser
        else HttpResponse("Unauthorised", status=403)
    )
    return response


def get_all_orders(request):
    pass


def get_order(request):
    pass
