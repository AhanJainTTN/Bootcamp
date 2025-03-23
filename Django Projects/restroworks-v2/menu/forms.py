from django import forms
from menu.models import MenuItem
from .validators import validate_image


class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = ["name", "description", "price", "image"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "input-field", "placeholder": "Enter item"}
            ),
            "description": forms.Textarea(
                attrs={"class": "input-field", "placeholder": "Enter description"}
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "input-field",
                    "placeholder": "Enter price",
                    "min": 0,
                }
            ),
            "image": forms.ClearableFileInput(),
        }
