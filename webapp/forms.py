from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
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


class ClientForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
        help_text="Enter your first name"
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
        help_text="Enter your last name"
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address"}),
        help_text="Enter a valid email address"
    )    
    phone = forms.CharField(
        max_length=30,
        label="Phone",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}),
        validators=[RegexValidator(r'^[\d\-\(\) ]+$', 'Enter a valid phone number.')],
        help_text="Format: 123-456-7890"
    )
    address = forms.CharField(
        max_length=100,
        label="Address",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Address"}),
        help_text="Enter your street address"
    )
    city = forms.CharField(
        max_length=30,
        label="City",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
        help_text="Enter your city"
    )
    state = forms.CharField(
        max_length=30,
        label="State",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
        help_text="Enter your state"
    )
    zip_code = forms.CharField(
        max_length=10,
        label="Zip Code",
        required=True,         
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Zip Code"}),
        validators=[RegexValidator(r'^\d{5}(?:[-\s]?\d{4})?$', 'Enter a valid zip code.')],
        help_text="Format: 12345 or 12345-6789"
    )

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name and last_name:
            if len(first_name + last_name) > 50:
                raise ValidationError("Combined name is too long (max 50 characters total)")
        state = cleaned_data.get('state')
        if state and len(state) != 2:
            raise ValidationError("Please use the 2-letter state abbreviation")
            
        return cleaned_data

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Remove all non-digit characters
        digits = ''.join(c for c in phone if c.isdigit())
        if len(digits) != 11:
            raise ValidationError("Phone number must contain exactly 10 digits")
        return phone

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            full_name = instance.full_name.split()
            initial = kwargs.setdefault('initial', {})
            initial['first_name'] = full_name[0]
            initial['last_name'] = ' '.join(full_name[1:])
        super().__init__(*args, **kwargs)
