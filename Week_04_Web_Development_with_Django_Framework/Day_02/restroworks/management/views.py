from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from management.models import Customer, Order, MenuItem


def get_menu_item_image(request):
    pass


def who_am_i(request):
    return HttpResponse(request.user)


def create_customer(request):
    pass


def get_all_customers(request):
    response = (
        HttpResponse(Customer.objects.all())
        if request.user.is_superuser
        else HttpResponse("Unauthorised", status=403)
    )

    # response = (
    #     HttpResponse(
    #         Customer.objects.filter(
    #             Q(first_name__istartswith="a") | Q(last_name__in=["Misra", "Nigam"])
    #         )
    #     )
    #     if request.user.is_superuser
    #     else HttpResponse("Unauthorised", status=403)
    # )

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
