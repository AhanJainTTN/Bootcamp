from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .forms import CustomerAuthenticationForm
from django.shortcuts import render


def user_login(request):
    form = CustomerAuthenticationForm()
    if request.method == "POST":
        form = CustomerAuthenticationForm(data=request.POST)
        if form.is_valid():
            return JsonResponse({"message": "Login successful."}, status=200)

    return render(request, "login.html", {"form_data": form})
