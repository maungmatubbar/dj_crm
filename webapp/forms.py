from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"})
    )    
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"})
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ["username", "password1", "password2"]:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
                "placeholder": self.fields[field].label
            })
