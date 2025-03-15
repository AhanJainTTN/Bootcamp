from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from rest_framework.decorators import api_view


@api_view(["POST"])
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response({"message": "Login successful."}, status=200)

        return Response({"error": "No user found."})
