from rest_framework import generics
from .models import Employees
from .serializers import EmployeeSerializer
from rest_framework.response import Response


# TODO: CRUD
# Create an Employee
# Read an Employee
# Read all Employees
# Update an Employee
# Delete all Employees


class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class AllEmployeesListView(generics.ListAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeUpdateView(generics.UpdateAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    partial = True


class EmployeeDeleteView(generics.DestroyAPIView):
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


def create_user(request):
    pass


def read_user(request):
    pass


def read_all_users(request):
    pass


def update_user(request):
    pass


def delete_user(request):
    pass
