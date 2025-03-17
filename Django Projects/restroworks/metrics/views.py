from django.shortcuts import render
from django.db.models import Sum, Avg, Count, F, Q, ExpressionWrapper, DecimalField
from .forms import DateRangeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from orders.models import Order, OrderItem
from customers.models import Customer
from menu.models import MenuItem
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from .forms import DateRangeForm


class MetricsView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    template_name = "metrics.html"
    form_class = DateRangeForm

    def test_func(self):
        # return True
        return self.request.user.is_staff

    def form_valid(self, form):
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]

        # Order Metrics
        orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
        total_order_count = orders.count()
        completed_order_count = orders.filter(status=3).count()
        cancelled_order_count = orders.filter(status=4).count()

        completed_revenue = (
            orders.filter(status=3)
            .aggregate(Sum("total_price"))
            .get("total_price__sum", 0)
        )

        average_order_value = (
            completed_revenue / completed_order_count if completed_order_count else 0
        )
        order_cancel_rate = (
            cancelled_order_count / total_order_count if total_order_count else 0
        )

        # Menu Item Metrics
        most_popular_item = (
            MenuItem.objects.annotate(
                order_count=Count("orderitem", filter=Q(orderitem__order__status=3))
            )
            .order_by("-order_count")
            .values("order_count", "name")
            .first()
        )

        most_popular_item_count = (
            most_popular_item.get("order_count")
            if most_popular_item.get("order_count")
            else 0
        )

        most_popular_item_name = (
            most_popular_item.get("name") if most_popular_item_count else "N/A"
        )

        top_item = (
            MenuItem.objects.annotate(
                total_revenue=Sum(
                    ExpressionWrapper(
                        F("orderitem__price") * F("orderitem__quantity"),
                        output_field=DecimalField(),
                    ),
                    filter=Q(orderitem__order__status=3),
                )
            )
            .order_by("-total_revenue")
            .values("name", "total_revenue")
            .first()
        )

        top_item_revenue = (
            top_item.get("total_revenue") if top_item.get("total_revenue") else 0
        )

        top_item_name = top_item.get("name") if top_item_revenue else "N/A"

        # Customer Metrics
        total_customer_count = Customer.objects.filter(
            user__date_joined__date__range=(start_date, end_date)
        ).count()

        metrics_data = {
            "Completed Revenue": f"₹{completed_revenue}",
            "Average Order Value": f"₹{average_order_value:.2f}",
            "Total Orders": total_order_count,
            "Completed Orders": completed_order_count,
            "Order Cancel Rate": f"{order_cancel_rate:.2f}",
            "Most Ordered": f"{most_popular_item_name} ({most_popular_item_count})",
            "Highest Revenue": f"{top_item_name} (₹{top_item_revenue})",
            "Customers Onboarded": total_customer_count,
        }

        return render(
            self.request,
            self.template_name,
            {
                "metrics": metrics_data,
                "start_date": start_date,
                "end_date": end_date,
                "form": form,
            },
        )

    def handle_no_permission(self):
        return JsonResponse({"error": "Unauthorized access."}, status=403)


# inheritance order matters in CBVs because Django resolves methods from left to right (MRO)
# if two parent classes define the same method, Django will use the method from the first parent listed in the class definition - wrong ordering may lead to unintended exposure of data
# class OrderMetricsView(LoginRequiredMixin, UserPassesTestMixin, FormView):
#     template_name = "metrics.html"
#     form_class = DateRangeForm

#     def test_func(self):
#         return self.request.user.is_staff

#     def form_valid(self, form):
#         start_date = form.cleaned_data["start_date"]
#         end_date = form.cleaned_data["end_date"]

#         orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
#         total_order_count = orders.count()
#         completed_order_count = orders.filter(status=3).count()
#         cancelled_order_count = orders.filter(status=4).count()

#         completed_revenue = (
#             orders.filter(status=3)
#             .aggregate(Sum("total_price"))
#             .get("total_price__sum", 0)
#         )

#         average_order_value = (
#             completed_revenue / completed_order_count if completed_order_count else 0
#         )
#         order_cancel_rate = (
#             cancelled_order_count / total_order_count if total_order_count else 0
#         )

#         metrics_data = {
#             "Completed Revenue": f"₹{completed_revenue}",
#             "Average Order Value": f"₹{average_order_value:.2f}",
#             "Total Orders": total_order_count,
#             "Completed Orders": completed_order_count,
#             "Order Cancel Rate": f"{order_cancel_rate:.2f}%",
#         }

#         return render(
#             self.request,
#             self.template_name,
#             {
#                 "metrics": metrics_data,
#                 "start_date": start_date,
#                 "end_date": end_date,
#                 "form": form,
#             },
#         )

#     def handle_no_permission(self):
#         return JsonResponse({"error": "Unauthorized access."}, status=403)


# class CustomerMetricsView(LoginRequiredMixin, UserPassesTestMixin, FormView):
#     template_name = "metrics.html"
#     form_class = DateRangeForm

#     def test_func(self):
#         return self.request.user.is_staff

#     def form_valid(self, form):
#         start_date = form.cleaned_data["start_date"]
#         end_date = form.cleaned_data["end_date"]

#         total_customer_count = Customer.objects.filter(
#             user__date_joined__date__range=(start_date, end_date)
#         ).count()

#         metrics_data = {
#             "New Customers Onboarded": total_customer_count,
#         }

#         return render(
#             self.request,
#             self.template_name,
#             {
#                 "metrics": metrics_data,
#                 "start_date": start_date,
#                 "end_date": end_date,
#                 "form": form,
#             },
#         )

#     def handle_no_permission(self):
#         return JsonResponse({"error": "Unauthorized access."}, status=403)


# class MenuItemMetricsView(LoginRequiredMixin, UserPassesTestMixin, FormView):
#     template_name = "metrics.html"
#     form_class = DateRangeForm

#     def test_func(self):
#         return self.request.user.is_staff

#     def form_valid(self, form):
#         start_date = form.cleaned_data["start_date"]
#         end_date = form.cleaned_data["end_date"]

#         most_popular_item = (
#             MenuItem.objects.annotate(order_count=Count("orderitem"))
#             .order_by("-order_count")
#             .values("order_count", "name")
#             .first()
#         )

#         most_popular_item_name = most_popular_item.get("name")
#         most_popular_item_count = most_popular_item.get("order_count")

#         from django.db.models import F, Sum, ExpressionWrapper, DecimalField

#         top_item = (
#             MenuItem.objects.annotate(
#                 total_revenue=Sum(
#                     ExpressionWrapper(
#                         F("orderitem__price") * F("orderitem__quantity"),
#                         output_field=DecimalField(),
#                     )
#                 )
#             )
#             .order_by("-total_revenue")
#             .values("name", "total_revenue")
#             .first()
#         )

#         top_item_name = top_item.get("name")
#         top_item_revenue = top_item.get("total_revenue")

#         metrics_data = {
#             "Most Ordered": f"{most_popular_item_name} ({most_popular_item_count} Times)",
#             "Highest Revenue": f"{top_item_name} (₹{top_item_revenue})",
#         }

#         return render(
#             self.request,
#             self.template_name,
#             {
#                 "metrics": metrics_data,
#                 "start_date": start_date,
#                 "end_date": end_date,
#                 "form": form,
#             },
#         )

#     def handle_no_permission(self):
#         return JsonResponse({"error": "Unauthorized access."}, status=403)


# @login_required
# def order_metrics(request):

#     if not request.user.is_staff:
#         return JsonResponse("error: Unauthorised access.", status=403)

#     if request.method == "POST":
#         form = DateRangeForm(request.POST)

#         if form.is_valid():
#             start_date = form.cleaned_data["start_date"]
#             end_date = form.cleaned_data["end_date"]

#         # TODO: Does this hit the database once and filters or is it queried each time?
#         # https://docs.djangoproject.com/en/5.2/topics/db/queries/#querysets-are-lazy
#         orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
#         total_order_count = orders.count()
#         completed_order_count = orders.filter(status=3).count()
#         cancelled_order_count = orders.filter(status=4).count()

#         completed_revenue = (
#             orders.filter(status=3)
#             .aggregate(Sum("total_price"))
#             .get("total_price__sum", "N/A")
#         )

#         try:
#             average_order_value = completed_revenue / completed_order_count
#             order_cancel_rate = cancelled_order_count / total_order_count

#         except Exception as e:
#             form.add_error(None, "No data available for the selected date range.")

#         metrics = {
#             "Completed Revenue": f"₹{completed_revenue}",
#             "Average Order Value": f"₹{average_order_value: .2f}",
#             "Total Orders": total_order_count,
#             "Completed Orders": completed_order_count,
#             "Order Cancel Rate": order_cancel_rate,
#         }

#         return render(
#             request,
#             "metrics.html",
#             {
#                 "metrics": metrics,
#                 "start_date": start_date,
#                 "end_date": end_date,
#                 "form": form,
#             },
#         )

#     form = DateRangeForm()
#     return render(request, "metrics.html", {"form": form})
