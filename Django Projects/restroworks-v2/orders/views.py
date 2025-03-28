from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from customers.models import Customer
from menu.models import MenuItem
from django.views.generic import ListView, DetailView, FormView
from .forms import OrderUpdateForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class CreateOrderView(LoginRequiredMixin, View):

    def post(self, request):
        customer = get_object_or_404(Customer, user=request.user)
        order = Order.objects.create(customer=customer)
        has_valid_items = False

        # request.POST gives a dictionary like object where the values are lists (since there can be multiple values for the same key).
        # request.POST.items() returns an iterator that provides a sequence of key-value pairs, but the values will be the first element in the list, not the entire list of values.
        # request.POST.items() essentially iterates over the dictionary and gives the first value for each key because it's designed to simplify the most common case, where there’s only one value for each key.
        # Use request.POST.getlist(key) to get all values for a key in the case of multiple values.
        for key, value in request.POST.items():
            if key == "csrfmiddlewaretoken":
                continue

            try:
                quantity = int(value)
                if quantity > 0:
                    menu_item = get_object_or_404(MenuItem, id=key)
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=quantity,
                        price=menu_item.price,
                    )
                    has_valid_items = True

            except (ValueError, MenuItem.DoesNotExist):
                continue

        if not has_valid_items:
            order.delete()
            messages.error(request, "Please select at least one valid menu item.")
            return redirect("/menu/view/all")

        order.calculate_total()
        return redirect(f"/orders/view/{order.id}")


class OrderDetailView(DetailView):
    template_name = "order_details.html"
    model = Order
    context_object_name = "order"


class OrderListView(ListView):
    template_name = "order_list.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        user = self.request.user
        status = self.request.GET.get("status")

        if user.is_staff:
            queryset = Order.objects.all()
        else:
            queryset = Order.objects.filter(customer__user=user)

        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by("-created_at")


class MenuItemFormView(FormView):
    template_name = "order_details.html"
    form_class = OrderUpdateForm

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, id=self.kwargs.get("order_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.order
        return context

    def form_valid(self, form):
        self.order.status = form.cleaned_data["status"]
        self.order.save(update_fields=["status"])
        return super().form_valid(form)

    def get_success_url(self):
        order_id = self.kwargs.get("order_id")
        return f"/orders/view/{order_id}"


@login_required
def track_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.customer.user and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    return JsonResponse({"order_id": order.id, "status": order.get_status_display()})
