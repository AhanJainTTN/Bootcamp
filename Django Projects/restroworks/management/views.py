from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q
from management.models import Customer, Order, MenuItem
from management.forms import CustomerForm

# To-Do
# CRUD for Customers
# Create a customer
# Read from DB data for a single customer
# Read from DB data for all customers
# Update details for a customer
# Delete a customer


def show_customer_form(request):
    return render(request, "index.html")


def add_customer(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CustomerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse("Registration successful.")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CustomerForm()

    return render(request, "index.html", {"form": form})


def get_customer(request, name):
    response = (
        HttpResponse(Customer.objects.get(first_name=name))
        if request.user.is_superuser
        else HttpResponse("Unauthorised", status=403)
    )
    return response


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


def update_customer(request):
    pass


def remove_customer(request):
    pass
