from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator


class ApplyDataForm(forms.Form):

    CHOICES = (
        ('mobile', 'mobile'),
        ('backend', 'backend'),
    )

    name = forms.CharField(max_length=256, required=True)
    email = forms.EmailField(max_length=256, required=True)
    phone = forms.CharField(max_length=14, required=True)
    full_address = forms.CharField(max_length=512, required=False)
    name_of_university = forms.CharField(max_length=256, required=True)
    graduation_year = forms.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2020)], required=True)
    cgpa = forms.FloatField(min_value=2.0, max_value=4.0, required=False)
    experience_in_months = forms.IntegerField(min_value=0, max_value=100, required=False)
    current_work_place_name = forms.CharField(max_length=256, required=False)
    applying_in = forms.Select(choices=CHOICES)
    applying_in = forms.CharField()
    expected_salary = forms.IntegerField(min_value=15000, max_value=60000, required=True)
    field_buzz_reference = forms.CharField(max_length=256, required=False)
    github_project_url = forms.CharField(max_length=512, required=True)
    cv_file = forms.FileField(validators=[FileExtensionValidator(['pdf'])])

class LoginForm(forms.Form):
    username = forms.EmailField(max_length=128, required=True)
    password = forms.CharField(widget=forms.PasswordInput())