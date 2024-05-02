from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput
from .models import Values


class add_data(ModelForm):
    class Meta:
        model = Values
        fields = ["name", "id", "dept", "email", "phone", "salary"]
        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "id": TextInput(attrs={"class": "form-control", "placeholder": "ID"}),
            "dept": TextInput(
                attrs={"class": "form-control", "placeholder": "Department"}
            ),
            "email": EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone": NumberInput(
                attrs={"class": "form-control", "placeholder": "Phone"}
            ),
            "salary": NumberInput(
                attrs={"class": "form-control", "placeholder": "Salary"}
            ),
        }
