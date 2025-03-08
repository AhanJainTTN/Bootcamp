from django.http import JsonResponse
from .forms import CustomerForm, CustomerAuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login


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
            # print(form)
            login(request, form.get_user())
            # redirect(reverse("menu:render_grid"))
            form = CustomerAuthenticationForm()
            # print("Redirecting...")
            return redirect(reverse("menu:render_grid"))
            # return JsonResponse({"message": "Login successful."}, status=200)

    return render(request, "login.html", {"form_data": form})


def render_home(request):
    return render(request, "home.html")
