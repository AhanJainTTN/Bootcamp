import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from customers.models import Customer
from menu.models import MenuItem
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


# filter() vs get()
# The difference is that filter returns a queryset object, wheras get returns the required object. If you use filter(), you typically do this whenever you expect more than just one object that matches your criteria. If no item was found matching your criteria, filter() returns am empty queryset without throwing an error.
@login_required
def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            customer_id = data.get("customer_id")
            customer = get_object_or_404(Customer, id=customer_id)

            # no need for atomic since user cannot order items which are not in menu
            # because the items are populated from frontend selections
            order = Order.objects.create(customer=customer, status=1)
            for item in data["items"]:
                menu_item = get_object_or_404(MenuItem, id=item["item_id"])
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=item["quantity"],
                    price=menu_item.price,
                )

            order.calculate_total()  # no need to save since calculate_total() already does that

            return JsonResponse(
                {"message": "Order created successfully", "order_id": order.id},
                status=201,
            )

        except Exception as e:
            return JsonResponse({"error": f"Error creating order: {e}"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


class CustomerOrderListView(ListView):
    template_name = "order_list.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(customer__user=self.request.user)


@login_required
def retrieve_all_customer_orders(request):
    orders = Order.objects.filter(customer__user=request.user)
    all_orders = []
    for order in orders:
        order_data = {
            "id": order.id,
            "customer": order.customer.id,
            "status": order.get_status_display(),
            "total_price": order.total_price,
            "items": [
                {
                    "menu_item": item.menu_item.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "total_price": item.total_price(),
                }
                for item in order.items.all()
            ],
            "created_at": order.created_at,
        }
        all_orders.append(order_data)

    return JsonResponse(all_orders, safe=False)


class OrderDetailView(DetailView):
    template_name = "order_detail.html"
    model = Order
    context_object_name = "order"


# @login_required
# def retrieve_order(request, order_id):

#     if request.user == order.customer.user or request.user.is_staff:
#         order = get_object_or_404(Order, id=order_id)
#         order_data = {
#             "id": order.id,
#             "customer": order.customer.id,
#             "status": order.get_status_display(),
#             "total_price": order.total_price,
#             "items": [
#                 {
#                     "menu_item": item.menu_item.name,
#                     "quantity": item.quantity,
#                     "price": item.price,
#                     "total_price": item.total_price(),
#                 }
#                 for item in order.items.all()
#             ],
#             "created_at": order.created_at,
#         }
#         return JsonResponse(order_data)

#     return JsonResponse({"error": "Unauthorized access"}, status=403)


class OrderListView(ListView):
    template_name = "order_list.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        return (
            Order.objects.filter(customer__user=self.request.user)
            if not self.request.user.is_staff
            else Order.objects.all()
        )


# @login_required
# def list_orders(request):
#     if not request.user.is_staff:
#         return JsonResponse({"error": "Unauthorized access"}, status=403)

#     orders = Order.objects.all().values(
#         "id", "customer_id", "status", "total_price", "created_at"
#     )
#     return JsonResponse(list(orders), safe=False)


# exclude(*args, **kwargs): Returns a new QuerySet containing objects that do not match the given lookup parameters.
@login_required
def list_active_orders(request):
    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    active_orders = Order.objects.filter(status__in=(1, 2)).values(
        "id", "customer_id", "status", "total_price", "created_at"
    )
    return JsonResponse(list(active_orders), safe=False)


@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            order.status = data.get("status", order.status)
            order.save()
            return JsonResponse({"message": "Order updated successfully"})
        except Exception as e:
            return JsonResponse({"error": f"Error updating order: {e}"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.customer.user and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    if request.method == "DELETE":
        order.delete()
        return JsonResponse({"message": "Order deleted successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.customer.user and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    if request.method == "PATCH":
        order.status = 4
        order.save()
        return JsonResponse({"message": "Order cancelled successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


@login_required
def track_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.user != order.customer.user and not request.user.is_staff:
        return JsonResponse({"error": "Unauthorized access"}, status=403)

    return JsonResponse({"order_id": order.id, "status": order.get_status_display()})
