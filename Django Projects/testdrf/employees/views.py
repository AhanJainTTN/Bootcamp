from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Employees
from .serializers import EmployeeSerializer


class EmployeeCreateView(generics.CreateAPIView):
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
