from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from .models import Employees
from .serializers import EmployeeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# ViewSet
class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


# Custom CBV
class CustomCBVEmployee(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id=None):
        if employee_id:
            employee = get_object_or_404(Employees, employee_id=employee_id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)

        employees = Employees.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, employee_id):
        employee = get_object_or_404(Employees, employee_id=employee_id)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, employee_id):
        employee = get_object_or_404(Employees, employee_id=employee_id)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, employee_id):
        employee = get_object_or_404(Employees, employee_id=employee_id)
        serializer = EmployeeSerializer(employee)
        employee.delete()
        # explicity show id since otherwise it displays null id
        # employee_id key after unpacking serialser.data else it will get overwritten with unpacked employee_id which was null
        return Response(
            {
                "deleted": {**serializer.data, "employee_id": employee_id},
                "message": "Employee deleted successfully",
            },
            status=204,
        )


# Excluding non required fields from PUT request payload does not violate
# When updating i.e. PUT or PATCH partial=True allows partial updates meaning only the provided fields are updated instead of requiring all fields. By default, DRF requires all fields in PUT requests.
# If any required field is missing, validation fails.
# many=True used when handling multiple objects
# Tells DRF to expect a list of objects instead of a single object
# without many=True, DRF expects a single dictionary {...}
# if a list is passed, DRF raises an error.
# if no explicit status code is provided in Response(), DRF assigns a default status code based on the HTTP method used
# GET: 200
# POST: 201
# PUT/PATCH: 200
# DELETE: 204
# When a request fails, DRF automatically assigns an appropriate HTTP status code unless overridden.


# Generic Concrete CBVs
class EmployeeCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class AllEmployeesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


# By default, only PUT and PATCH are allowed
# We can pass a full resource through PATCH as well
class EmployeeUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    partial = True


class EmployeeDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
