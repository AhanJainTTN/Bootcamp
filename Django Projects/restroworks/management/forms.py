from django import forms


class CustomerForm(forms.Form):
    first_name = forms.CharField(label="Your name", max_length=100)
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    phone = forms.IntegerField()
    email = forms.EmailField(max_length=255)
