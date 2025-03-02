import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from customers.models import Customer


def customer_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        # why filter and not get
        # filter(username=username).exists() only checks if a record exists and returns True or False
        # get(username=username) retrieves the entire user object, which is unnecessary if we just need to check existence
        # get() rraises an Error If No Match Is Found
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        try:
            # why use atomic? - to ensure rollback on failure - why? - if a user enters a phone number which already exists, this raises an IntegrityError and no user is added to the Customers table - however since we are adding to the user table before, the user does get added to auth_user - we want to ensuure a user only gets added to auth_user if no IntegrityError is raised - why not just check for unique phone number? - defeats the point of using integrity constraints while using models and also not very scalable - not reasonable to find and check each field if our model had a lot of fields
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )
                customer = Customer.objects.create(user=user, phone=phone)

                return JsonResponse(
                    {
                        "message": "Customer registered successfully",
                        "customer_id": customer.id,
                    },
                    status=201,
                )

        except IntegrityError:
            return JsonResponse(
                {"error": "Integrity error, registration failed"}, status=400
            )

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def retrieve_customer(request, customer_id):
    # get_object_or_404(): calls get() on a given model manager, but it raises Http404 instead of the model’s DoesNotExist exception.
    customer = get_object_or_404(Customer, id=customer_id)

    # request.user returns the model instance logged-in user can retrieve only their own profile
    if request.user == customer.user or request.user.is_staff:
        return JsonResponse(
            {
                "id": customer.id,
                "username": customer.user.username,
                "email": customer.user.email,
                "phone": customer.phone,
                "created_at": customer.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return JsonResponse({"error": "Unauthorized access"}, status=403)


@login_required
def list_customers(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    customers = Customer.objects.all().values(
        "id", "user__username", "user__email", "phone"
    )
    return JsonResponse(list(customers), safe=False)


# request.POST does not work for PUT - why - request.POST only works for POST requests with application/x-www-form-urlencoded or multipart/form-data. Django does not populate request.POST for PUT, PATCH, or DELETE requests, even if the request contains form-data.
@login_required
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.user == customer.user or request.user.is_staff:
        # request.POST is empty for PUT request so load data from request.body
        if request.method == "PUT":
            # expects data in raw JSON in request body - formdat
            data = json.loads(request.body)
            customer.user.username = data.get("username", customer.user.username)
            customer.user.email = data.get("email", customer.user.email)
            customer.phone = data.get("phone", customer.phone)

            try:
                with transaction.atomic():
                    customer.user.save()
                    customer.save()

                    return JsonResponse({"message": "Customer updated successfully"})

            except IntegrityError as e:
                return JsonResponse(
                    {"error": "Integrity error, failed to update user."}, status=400
                )

        return JsonResponse({"error": "Invalid request method"}, status=405)

    return JsonResponse({"error": "Unauthorized access"}, status=403)


@login_required
def delete_customer(request, customer_id):
    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    if request.method == "DELETE":
        customer = get_object_or_404(Customer, id=customer_id)
        customer.user.delete()
        return JsonResponse({"message": "Customer deleted successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=405)
