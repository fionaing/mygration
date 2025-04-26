from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms

from home.models import Plan


class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ["name", "location", "description", "image"]
        widgets = {
            "name":        forms.TextInput(attrs={"class": "form-control"}),
            "location":    forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "image":       forms.ClearableFileInput(attrs={"class": "form-control"}),
        }