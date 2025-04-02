from django.shortcuts import render
from django.db.models import Sum, Count, F, Q, ExpressionWrapper, DecimalField
from .forms import DateRangeForm
from django.http import JsonResponse
from orders.models import Order
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
        return self.request.user.is_staff

    def form_valid(self, form):
        start_date = form.cleaned_data["start_date"]
        end_date = form.cleaned_data["end_date"]

        # Order Metrics
        # TODO: Improve performance - DONE
        # orders = Order.objects.filter(created_at__date__range=(start_date, end_date))
        # total_order_count = orders.count()
        # completed_order_count = orders.filter(status=3).count()
        # cancelled_order_count = orders.filter(status=4).count()
        # completed_revenue = (
        #     orders.filter(status=3)
        #     .aggregate(Sum("total_price"))
        #     .get("total_price__sum", 0)
        # )

        order_metrics = Order.objects.filter(
            created_at__date__range=(start_date, end_date)
        ).aggregate(
            total_order_count=Count("id"),
            completed_order_count=Count("id", filter=Q(status=3)),
            cancelled_order_count=Count("id", filter=Q(status=4)),
            completed_revenue=Sum("total_price", filter=Q(status=3)),
        )

        total_order_count = order_metrics.get("total_order_count", 0)
        completed_order_count = order_metrics.get("completed_order_count", 0)
        cancelled_order_count = order_metrics.get("cancelled_order_count", 0)
        completed_revenue = order_metrics.get("completed_revenue", 0)

        average_order_value = (
            completed_revenue / completed_order_count if completed_order_count else 0
        )
        order_cancel_rate = (
            cancelled_order_count / total_order_count if total_order_count else 0
        )

        # Menu Item Metrics
        most_popular_item = (
            MenuItem.objects.annotate(
                order_count=Count(
                    "order_item",
                    filter=Q(
                        order_item__order__status=3,
                        created_at__date__range=(start_date, end_date),
                    ),
                )
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

        # works without ExpressionWrapper bevause DB automatically resolves the type
        # good practice to leave it on if using two values with different types
        top_item = (
            MenuItem.objects.annotate(
                total_revenue=Sum(
                    ExpressionWrapper(
                        F("order_item__price") * F("order_item__quantity"),
                        output_field=DecimalField(),
                    ),
                    filter=Q(
                        order_item__order__status=3,
                        created_at__date__range=(start_date, end_date),
                    ),
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

    # by default shows a 403 forbidden page (if not overridden)
    def handle_no_permission(self):
        return JsonResponse({"error": "Unauthorized access."}, status=403)
