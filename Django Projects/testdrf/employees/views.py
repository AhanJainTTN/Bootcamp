import json
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from employees.serializers import EmployeeSerializer
from employees.models import Employees, Jobs

"""
API Endpoints for Employee Management:

    GET /employees/
    Retrieve a list of all employees.

    GET /employees/<int:id>/
    Retrieve details of a specific employee by ID.

    POST /employees/
    Create a new employee.

    PUT /employees/<int:id>/
    Fully update an existing employee by ID.

    PATCH /employees/<int:id>/
    Partially update an existing employee by ID.

    DELETE /employees/<int:id>/
    Delete an employee by ID.

TODO: Implement each of these endpoints using all available methods in Django and Django REST Framework (DRF).

Django (Core)
    Function Based Views
    Class Based Views (CBVs)
        Custom CBVs
        Generic CBVs
        Mixins
"""

# Django (Core) - CBV - Custom CBV
from django.views import View
from django.forms.models import model_to_dict


class EmployeeView(View):

    def get(self, request, employee_id=None):
        if employee_id:
            employee = get_object_or_404(Employees, employee_id=employee_id)
            # .values() equivalent for a single object
            employee = model_to_dict(employee)
            return JsonResponse(employee)

        # Django model instances (<Employee1>) are not JSON serializable by default .values() is needed to convert to QuerySet object which is JSON serializable when wrapped with list()
        # without .values():
        # <class 'django.db.models.query.QuerySet'>
        # <QuerySet [<Employees: Employees object (206)>]>
        # with .values():
        # <class 'django.db.models.query.QuerySet'>
        # <QuerySet [{'first_name': 'William'}]>
        # values vs values_list: Only values in values_list
        # both keys and values in values
        employees = (
            Employees.objects.all()
            .order_by("-employee_id")
            .values("employee_id", "first_name", "last_name", "hire_date")
        )
        # why list() - converts lazy QuerySet to dictionary
        # A QuerySet is lazy and not inherently serializable to JSON
        # JsonResponse expects a dictionary by default, or a serializable list if safe=False
        return JsonResponse(list(employees), safe=False)

    def post(self, request):
        data = json.loads(request.body)
        data["job"] = get_object_or_404(Jobs, job_id=data["job"])
        data["manager"] = get_object_or_404(Employees, employee_id=data["manager"])
        employee = Employees.objects.create(**data)

        return JsonResponse({"created": model_to_dict(employee)})

    # why filter? - Getting a single object using get returns a model instance
    # this model instance has no update method
    # update method exists only for QuerySets
    # why .values() here -> to make list(employee) JSON serializable for to show updated object
    # update itself can take place with/without .values()
    # alternate is to retrieve object again and use model_to_dict
    def patch(self, request, employee_id):
        # equivalent to list(queryset.filter(*args, **kwargs))
        # does not work since no .update() on a list
        # employee = get_list_or_404(Employees, employee_id=employee_id)

        # employee = Employees.objects.filter(employee_id=employee_id).values("email")
        employee = Employees.objects.filter(employee_id=employee_id)

        if employee:
            data = json.loads(request.body)
            employee.update(**data)
            employee = model_to_dict(employee.first())

            return JsonResponse(employee)

        return JsonResponse({"error": "No employee found."}, status=404)

    def put(self, request, employee_id):
        employee = Employees.objects.filter(employee_id=employee_id)

        if employee:
            data = json.loads(request.body)
            data["employee_id"] = employee_id

            required_fields = {
                f.name for f in Employees._meta.get_fields() if not f.is_relation
            }

            if not all(field in data for field in required_fields):
                return JsonResponse(
                    {"error": "Missing required fields for full update."}, status=400
                )

            employee.update(**data)
            employee = model_to_dict(employee.first())

            return JsonResponse(employee)

        return JsonResponse({"error": "No employee found."}, status=404)

    def delete(self, request, employee_id):
        employee = get_object_or_404(Employees, employee_id=employee_id)
        employee_id = employee.employee_id
        employee.delete()

        return JsonResponse(
            {"deleted": {**model_to_dict(employee), "employee_id": employee_id}}
        )


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
