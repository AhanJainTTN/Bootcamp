import json
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, get_list_or_404, render
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

Django (DRF)
    Function Based Views
    Class Based Views (CBVs)
        Custom CBVs
        Generic CBVs
        Mixins
"""
# Django (Core) - Generic CBVs
# https://docs.djangoproject.com/en/5.1/ref/class-based-views/generic-display/#generic-display-views
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)


class EmployeeDetailView(DetailView):
    model = Employees
    template_name = "employees_detail.html"
    context_object_name = "employee"


class EmployeeListView(ListView):
    model = Employees
    template_name = "employees_list.html"
    context_object_name = "employees"


# A view that displays a form for creating an object, redisplaying the form with validation errors (if there are any) and saving the object. By default, looks for a template with model_form.html (employees_form.html)
class EmployeeCreateView(CreateView):
    model = Employees
    fields = "__all__"
    template_name = "employees_form.html"

    # saves the object and redirects to success_url
    # here overridden because we just want to render a success template directly
    # without creating a new view for it
    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, "success.html")


class EmployeeUpdateView(UpdateView):
    model = Employees
    template_name = "employees_form.html"
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, "success.html")


class EmployeeDeleteView(DeleteView):
    model = Employees
    template_name = "employees_form.html"
    fields = "__all__"

    def form_valid(self, form):
        self.object.delete()
        return render(self.request, "success.html")


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

    # request.POST vs request.body
    # request.POST used for form data (application/x-www-form-urlencoded or multipart/form-data)
    # Works automatically for form submissions (e.g., from HTML forms).
    # Django parses the body and populates request.POST as a dictionary-like object (QueryDict)
    # Only works for POST requests with form-encoded data
    # request.body used for raw request payload (bytes), regardless of method (POST, PUT, PATCH, etc.).
    # must be manually decoded and parsed.
    # Works for any HTTP method.
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
class EmployeeCreateViewDRF(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailViewDRF(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


class AllEmployeesListViewDRF(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer


# By default, only PUT and PATCH are allowed
# We can pass a full resource through PATCH as well
class EmployeeUpdateViewDRF(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    partial = True


class EmployeeDeleteViewDRF(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
