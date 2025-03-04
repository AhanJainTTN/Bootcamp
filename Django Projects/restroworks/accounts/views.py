from django.http import JsonResponse
from .forms import CustomerForm, CustomerAuthenticationForm
from django.shortcuts import render


def user_signup(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            if customer:
                form = CustomerForm()
                # return JsonResponse(
                #     {
                #         "message": "Customer registered successfully",
                #         "customer_id": customer.id,
                #     },
                #     status=201,
                # )

    return render(request, "signup.html", {"form_data": form})


def user_login(request):
    form = CustomerAuthenticationForm()
    if request.method == "POST":
        form = CustomerAuthenticationForm(data=request.POST)
        if form.is_valid():
            form = CustomerAuthenticationForm()
            # return JsonResponse({"message": "Login successful."}, status=200)

    return render(request, "login.html", {"form_data": form})
