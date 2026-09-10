from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Transaction


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["type", "category", "amount", "date", "description"]
        widgets = {
            "type": forms.Select(attrs={"class": "form-control", "id": "id_type"}),
            "category": forms.Select(attrs={"class": "form-control", "id": "id_category"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional note"}),
        }
