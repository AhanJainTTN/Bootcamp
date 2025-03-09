from django.http import JsonResponse
from .forms import CustomerForm, CustomerAuthenticationForm, ExcelForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from openpyxl import Workbook, load_workbook
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from customers.models import Customer
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError


# Lifecycle of a FormView:
# 1. User requests the form page (GET /upload-excel/).
# 2. Django initializes the FormView.
# 3. get() method runs, calling get_context_data().
# 4. The form is rendered in the template.
# 5. User submits the form (POST request) with data.
# 6. Django runs form_valid() if validation passes, or form_invalid() if it fails.
# If valid: Custom processing logic runs. Django redirects to get_success_url(), unless overridden.
# If invalid: Re-renders the form with error messages.
class BulkUploadForm(FormView):
    template_name = "excel_form.html"
    form_class = ExcelForm
    success_url = "/menu/view/grid/"

    def form_valid(self, form):
        excel_file = form.cleaned_data["excel_file"]
        expected_headers = (
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "phone",
        )

        try:
            wb = load_workbook(excel_file)
            ws = wb.active
            sheet_headers = tuple(cell.value for cell in ws[1])

            if sheet_headers != expected_headers:
                form.add_error(
                    None,
                    f"Sheet headers do not match the expected format: {expected_headers}",
                )
                return self.form_invalid(form)

            curr_row = 1
            created_count = 0

            for row in ws.iter_rows(min_row=2, values_only=True):
                curr_row += 1
                # Skip headers
                username, password, first_name, last_name, email, phone = row

                if not all(row):
                    form.add_error(None, f"Row {curr_row}: Null values encountered.")
                    continue

                try:
                    validate_password(password)
                    user = User(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                    )
                    print(email)
                    user.set_password(password)
                    with transaction.atomic():
                        user.save()
                        print(user)
                        customer = Customer.objects.create(
                            user=user, email=email, phone=phone
                        )
                        created_count += 1
                        print(customer)

                except (IntegrityError, ValidationError) as e:
                    form.add_error(None, f"Row {curr_row}: {str(e)}")

            if form.non_field_errors():
                return self.form_invalid(form)

            total_entries = ws.max_row - 1
            summary = f"Total Entries: {total_entries}\nNew Entries: {created_count}\nErrors:\n{errors}"
            print(summary)

        except Exception as e:
            form.add_error(None, f"Error processing file: {str(e)}")
            return self.form_invalid(form)

        # ensures that the default behavior of form_valid() is executed, which redirects the user to the success URL (get_success_url()).
        return super().form_valid(form)


@login_required
def create_from_excel(request):
    return render(request, "excel_form.html")


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


errors = {
    1: "Error processing 1: ['This password is too short. It must contain at least 8 characters.']",
    2: "Error processing 2: UNIQUE constraint failed: auth_user.username",
    3: "Error processing 3: UNIQUE constraint failed: customers_customer.email",
    4: "Error processing 4: UNIQUE constraint failed: customers_customer.email",
    5: "Error processing 5: UNIQUE constraint failed: customers_customer.email",
    6: "Error processing 6: UNIQUE constraint failed: customers_customer.email",
    7: "Error processing 7: Null values encountered.",
    8: "Error processing 8: UNIQUE constraint failed: customers_customer.email",
    9: "Error processing 9: UNIQUE constraint failed: customers_customer.email",
    10: "Error processing 10: UNIQUE constraint failed: customers_customer.email",
    11: "Error processing 11: Null values encountered.",
    12: "Error processing 12: UNIQUE constraint failed: customers_customer.email",
    13: "Error processing 13: UNIQUE constraint failed: customers_customer.email",
    14: "Error processing 14: Null values encountered.",
    15: "Error processing 15: UNIQUE constraint failed: customers_customer.email",
    16: "Error processing 16: UNIQUE constraint failed: customers_customer.email",
    17: "Error processing 17: UNIQUE constraint failed: customers_customer.email",
    18: "Error processing 18: UNIQUE constraint failed: customers_customer.email",
    19: "Error processing 19: UNIQUE constraint failed: customers_customer.email",
    20: "Error processing 20: UNIQUE constraint failed: customers_customer.email",
    21: "Error processing 21: UNIQUE constraint failed: customers_customer.email",
    22: "Error processing 22: UNIQUE constraint failed: customers_customer.email",
    23: "Error processing 23: UNIQUE constraint failed: customers_customer.email",
    24: "Error processing 24: UNIQUE constraint failed: customers_customer.email",
    25: "Error processing 25: UNIQUE constraint failed: customers_customer.email",
    26: "Error processing 26: UNIQUE constraint failed: customers_customer.email",
    27: "Error processing 27: UNIQUE constraint failed: customers_customer.email",
    28: "Error processing 28: UNIQUE constraint failed: customers_customer.email",
    29: "Error processing 29: UNIQUE constraint failed: customers_customer.email",
    30: "Error processing 30: UNIQUE constraint failed: customers_customer.email",
    31: "Error processing 31: UNIQUE constraint failed: customers_customer.email",
    32: "Error processing 32: UNIQUE constraint failed: customers_customer.email",
    33: "Error processing 33: UNIQUE constraint failed: customers_customer.email",
    34: "Error processing 34: UNIQUE constraint failed: customers_customer.email",
    35: "Error processing 35: UNIQUE constraint failed: customers_customer.email",
    36: "Error processing 36: UNIQUE constraint failed: customers_customer.email",
    37: "Error processing 37: UNIQUE constraint failed: customers_customer.email",
    38: "Error processing 38: UNIQUE constraint failed: customers_customer.email",
    39: "Error processing 39: UNIQUE constraint failed: customers_customer.email",
    40: "Error processing 40: UNIQUE constraint failed: customers_customer.email",
    41: "Error processing 41: UNIQUE constraint failed: customers_customer.email",
    42: "Error processing 42: UNIQUE constraint failed: customers_customer.email",
    43: "Error processing 43: UNIQUE constraint failed: customers_customer.email",
    44: "Error processing 44: UNIQUE constraint failed: customers_customer.email",
    45: "Error processing 45: UNIQUE constraint failed: customers_customer.email",
    46: "Error processing 46: UNIQUE constraint failed: customers_customer.email",
    47: "Error processing 47: UNIQUE constraint failed: customers_customer.email",
    48: "Error processing 48: UNIQUE constraint failed: customers_customer.email",
    49: "Error processing 49: UNIQUE constraint failed: customers_customer.email",
    50: "Error processing 50: UNIQUE constraint failed: customers_customer.email",
}
