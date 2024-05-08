from django import forms
from django.forms import ModelForm, TextInput, EmailInput, NumberInput
from .models import Database


class add_data(ModelForm):
    class Meta:
        model = Database
        fields = [
            "name",
            "id",
            "dept",
            "salary",
            "designation",
            "gender",
            "pan_no",
            "aadhar_no",
            "dateofbirth",
            "dateofjoining",
            "bankname",
            "ac_no",
            "uan_no",
        ]
        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "id": TextInput(attrs={"class": "form-control", "placeholder": "ID"}),
            "dept": TextInput(
                attrs={"class": "form-control", "placeholder": "Department"}
            ),
            "salary": NumberInput(
                attrs={"class": "form-control", "placeholder": "Salary"}
            ),
            "designation": TextInput(
                attrs={"class": "form-control", "placeholder": "Designation"}
            ),
            "gender": TextInput(
                attrs={"class": "form-control", "placeholder": "Gender"}
            ),
            "pan_no": TextInput(
                attrs={"class": "form-control", "placeholder": "Pan Number"}
            ),
            "aadhar_no": TextInput(
                attrs={"class": "form-control", "placeholder": "Aadhar Number"}
            ),
            "dateofbirth": TextInput(
                attrs={"class": "form-control", "placeholder": "Date Of Birth"}
            ),
            "dateofjoining": TextInput(
                attrs={"class": "form-control", "placeholder": "Date Of Joining"}
            ),
            "bankname": TextInput(
                attrs={"class": "form-control", "placeholder": "Bank Name"}
            ),
            "ac_no": NumberInput(
                attrs={"class": "form-control", "placeholder": "Account Number"}
            ),
            "uan_no": NumberInput(
                attrs={"class": "form-control", "placeholder": "UAN Number"}
            ),
        }
        labels = {
            "dateofbirth": "Date Of Birth",
            "dateofjoining": "Date Of Joining",
            "bankname": "Bank Name",
            "ac_no": "Account Number",
            "uan_no": "UAN Number",
        }
