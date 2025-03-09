import json
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from menu.models import MenuItem
from menu.forms import MenuItemForm
from orders.models import Order, OrderItem
from customers.models import Customer
from django.views.generic.edit import FormView
from django.views import View

# using get instead of indexing operator so model itself handles IntegrityError
# using indexing operator (will necessitate handling a KeyError) or explicit NULL checks is redundant
# Fat Model, Thin Views
# login_required is not redundant here - why? - login_required only ensures a user is authenticated and does not check permissions - it also redirects to the login page if not authenticated
# we still need to explicity check if a staff member is creating the menu item
# @login_required
# def create_item(request):

#     if request.user.is_staff:

#         if request.method == "POST":

#             try:
#                 MenuItem.objects.create(
#                     name=request.POST.get("name"),
#                     description=request.POST.get("description"),
#                     price=request.POST.get("price"),
#                     image=request.FILES.get("image"),
#                 )

#                 return JsonResponse({"message": "Item successfully added."})

#             except IntegrityError as e:
#                 return JsonResponse({"error": f"Error while adding item. {e}"})

#         return JsonResponse({"error": "Invalid request method."}, status=405)

#     return JsonResponse({"error": "Unauthorised access."}, status=403)


# must override form_valid to save instance
# else django just validates the form
# alternate - use CreateView if working with ModelForm
class MenuItemFormView(FormView):
    template_name = "menu-item_form.html"
    form_class = MenuItemForm
    success_url = "/menu/view/all"

    # context_object_name = "form_data" # does not work with FormView and CreateView
    def form_valid(self, form):
        form.save()  # Explicitly save the object
        return super().form_valid(form)


class MenuItemCreateView(View):
    template_name = "menu-item_form.html"

    def get(self, request):
        form = MenuItemForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = MenuItemForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/menu/view/all")

        return render(request, self.template_name, {"form": form})


# with form
# @login_required
# def create_item(request):
#     if not request.user.is_staff:
#         return JsonResponse({"error": "Unauthorised access."}, status=403)

#     form = MenuItemForm()
#     if request.method == "POST":
#         form = MenuItemForm(request.POST, request.FILES)

#         if form.is_valid():
#             item = form.save()
#             if item:
#                 form = MenuItemForm()
#             # return JsonResponse({"message": "Item successfully added."})

#     return render(request, "menu-item_form.html", {"form_data": form})


# DetailView makes it more convenient to get a single item
# Override get() method to customise object retrieval
# Override get_context_data() to customise context data sent to template
class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = "menuitem.html"
    context_object_name = "menu_item"


# def retrieve_item(request, item_id):
#     item = get_object_or_404(MenuItem, id=item_id)
#     return JsonResponse(
#         {
#             "id": item.id,
#             "name": item.name,
#             "description": item.description,
#             "rating": item.rating,
#             # "price": str(item.price),
#             "price": item.price,  # why str - DecimalField stores values as decimal.Decimal, which is not natively serializable by json module - "price": item.price causes TypeError
#             "image_url": item.image.url if item.image else None,
#             "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
#             "updated_at": item.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
#         }
#     )


# create() vs save()
# objects.create(): creates and saves in one step - creates a new object automatically
# objects.save(): saves an existing or new object - does not create a new object automatically (you must instantiate it first) - mainly used if received values are to be modified or for updating existing objects


# objects.all() vs objects.all().values(...)
# MenuItem.objects.all(): returns a QuerySet of model instances, which are not directly JSON serializable.
# MenuItem.objects.all().values(...): returns a QuerySet of dictionaries, which are JSON serializable.
# ImageField stores the image file path, not the actual image. When queried using .values("image"), it returns the relative file path, not the image itself.
# use with settings.MEDIA_URL to get the full url: settings.MEDIA_URL + item["image"]


# ListView makes displaying a list of objects convenient
# Override get_queryset() method to customise object retrieval
# Override get_context_data() to customise context data sent to template
class MenuItemListView(ListView):
    template_name = "menuitem_list.html"
    paginate_by = 2  # adding pagination
    model = MenuItem
    context_object_name = "menu_items"


# def list_items(request):
#     # returns a list of dictionaries, which is JSON serializable.
#     items = MenuItem.objects.all().values(
#         "id", "name", "description", "rating", "price", "image"
#     )
#     # safe=False: https://www.django-antipatterns.com/antipattern/return-a-jsonresponse-with-safe-false.html
#     # The safe boolean parameter defaults to True. If it’s set to False, any object can be passed for serialization (otherwise only dict instances are allowed). If safe is True and a non-dict object is passed as the first argument, a TypeError will be raised.
#     return JsonResponse(list(items), safe=False)


# Why POST and not PUT - images are sent in request.FILES which does not work with PUT
@login_required
def update_item(request, item_id):

    if request.user.is_staff:

        if request.method == "POST":

            item = get_object_or_404(MenuItem, id=item_id)

            try:

                item.name = request.POST.get("name", item.name)
                item.description = request.POST.get("description", item.description)
                item.price = request.POST.get("price", item.price)
                item.image = request.FILES.get("image", item.image)
                item.save()

                return JsonResponse({"message": "Item successfully updated."})

            except IntegrityError as e:
                return JsonResponse({"error": f"Error while updating item. {e}"})

        return JsonResponse({"error": "Invalid request method."}, status=405)

    return JsonResponse({"error": "Unauthorised access."}, status=403)


@login_required
def delete_item(request, item_id):

    if request.user.is_staff:

        item = get_object_or_404(MenuItem, id=item_id)

        if request.method == "DELETE":
            item.delete()
            return JsonResponse({"message": "Item deleted successfully"})

        return JsonResponse({"error": "Invalid request method"}, status=405)

    return JsonResponse({"error": "Unauthorized access"}, status=403)


@login_required
def render_grid(request):
    menu_items = MenuItem.objects.all()
    if request.method == "POST":
        customer = Customer.objects.get(user=request.user)
        order = Order.objects.create(customer=customer)
        for item_id, quantity in dict(request.POST).items():
            if item_id != "csrfmiddlewaretoken":
                menu_item = MenuItem.objects.get(id=item_id)
                order_item = OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity[0],
                    price=menu_item.price,
                )

        order.calculate_total()
        return JsonResponse(
            {"message": f"Order with id {order.id} created successfully."}
        )
    return render(request, "menu-item_grid.html", {"menu_items": menu_items})
