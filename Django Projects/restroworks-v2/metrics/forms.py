from django import forms
from django.core.exceptions import ValidationError


class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"class": "input-field", "type": "date"}),
    )
    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"class": "input-field", "type": "date"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be later than end date.")

        return cleaned_data
