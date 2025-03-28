import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from customers.models import Customer


@login_required
def retrieve_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    if request.user == customer.user or request.user.is_staff:
        return JsonResponse(
            {
                "id": customer.id,
                "username": customer.user.username,
                "email": customer.user.email,
                "phone": customer.phone,
                "created_at": customer.created_at,
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
