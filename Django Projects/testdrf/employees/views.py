from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Employees
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from rest_framework.request import Request
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


class EmployeeCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class AllEmployeesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    partial = True


class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
