from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from menu.models import MenuItem
from menu.forms import MenuItemForm
from orders.models import Order, OrderItem
from customers.models import Customer
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages


"""
GET
/ : Get all (template: menuitem_list.html)
/<int: id> : Get one (template: menuitem_detail.html)
/add/: show form to add (template: menuitem_form.html)

POST
/: place order
/add/: Create one

PUT
/<int: id>

PATCH
/<int: id>

DELETE
/<int: id>
"""


class MenuItemListView(LoginRequiredMixin, ListView):
    model = MenuItem
    template_name = "menuitem_list.html"
    context_object_name = "menu_items"
    paginate_by = 16


class MenuItemDetailView(DetailView):
    model = MenuItem
    template_name = "menuitem_detail.html"
    context_object_name = "item"


class MenuItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "menuitem_form.html"
    success_url = "/menu/view/all"

    def test_func(self):
        return self.request.user.is_staff


class MenuItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = "menuitem_form.html"

    def get_success_url(self):
        return f"/menu/view/{self.kwargs["pk"]}/"

    def test_func(self):
        return self.request.user.is_staff


class MenuItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = MenuItem
    success_url = "menuitem_list.html"

    def test_func(self):
        return self.request.user.is_staff


@login_required
def delete_item(request, item_id):

    if request.user.is_staff:
        item = get_object_or_404(MenuItem, id=item_id)
        item_name = item.name
        item.delete()
        messages.success(request, f"'{item_name}' was deleted successfully.")
        return redirect("/menu/view/all")

    return JsonResponse({"error": "Unauthorized access"}, status=403)
