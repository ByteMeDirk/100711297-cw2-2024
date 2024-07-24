from django import forms
from django.contrib.auth.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    """
    Custom Task Form that extends the ModelForm.
    """

    class Meta:
        model = Task
        fields = ["title", "description", "due_date"]
        widgets = {
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title",
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
            }
        )
    )

    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control",
                "placeholder": "Due Date",
                "type": "datetime-local",
            }
        )
    )

    owner = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )
