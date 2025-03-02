from django.http import HttpResponse

# from django.shortcuts import render, redirect
# from django.db.models import Q
# from management.models import Customer, Order, MenuItem
# from management.forms import CustomerForm, MenuItemForm
# from django.urls import reverse

# # To-Do
# # CRUD for Customers
# # Create a customer
# # Read from DB data for a single customer
# # Read from DB data for all customers
# # Update details for a customer
# # Delete a customer


def success_page(request):
    return HttpResponse("Request successful.")


# # Source: https://docs.djangoproject.com/en/5.1/topics/forms/
# def add_customer(request):
#     if request.method == "POST":
#         # create a form instance and populate it with data from the request:
#         customer_form = CustomerForm(request.POST)
#         # check whether it's valid:
#         if customer_form.is_valid():
#             # process the data in form.cleaned_data as required - why clean a form - Each field in a Form class is responsible not only for validating data, but also for “cleaning” it – normalizing it to a consistent format.
#             # https://stackoverflow.com/questions/53594745/what-is-the-use-of-cleaned-data-in-django
#             # https://docs.djangoproject.com/en/5.1/ref/forms/api/#django.forms.Form.cleaned_data
#             # redirect to a new URL
#             cleaned_data = customer_form.cleaned_data
#             print(cleaned_data)
#             # print(type(cleaned_data), cleaned_data) # <class 'dict'>
#             return redirect("success_page")  # redirect to common success page
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         customer_form = CustomerForm()
#     # Why {"form": form} Instead of just form - when rendering a template using render(), the context (data sent to the template) must be a dictionary
#     return render(request, "customer_form.html", {"form": customer_form})


# def get_customer(request, name):
#     response = (
#         HttpResponse(Customer.objects.get(first_name=name))
#         if request.user.is_superuser
#         else HttpResponse("Unauthorised", status=403)
#     )
#     return response


# def get_all_customers(request):
#     response = (
#         HttpResponse(Customer.objects.all())
#         if request.user.is_superuser
#         else HttpResponse("Unauthorised", status=403)
#     )

#     # response = (
#     #     HttpResponse(
#     #         Customer.objects.filter(
#     #             Q(first_name__istartswith="a") | Q(last_name__in=["Misra", "Nigam"])
#     #         )
#     #     )
#     #     if request.user.is_superuser
#     #     else HttpResponse("Unauthorised", status=403)
#     # )

#     return response


# def add_menu_item(request):
#     if request.method == "POST":
#         menu_item_form = MenuItemForm(request.POST, request.FILES)
#         print("Files: ", request.FILES)
#         if menu_item_form.is_valid():
#             print("Valid Form.")
#             cleaned_data = menu_item_form.cleaned_data
#             print("Cleaned Data: ", cleaned_data)
#             menu_item_form.save()

#             return redirect("success_page")
#         else:
#             print("Errors: ", menu_item_form.errors)
#     else:
#         menu_item_form = MenuItemForm()

#     return render(request, "menu-item_form.html", {"form": menu_item_form})


# def update_customer(request):
#     pass


# def remove_customer(request):
#     pass
