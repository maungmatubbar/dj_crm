from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import Client, Product, Service
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



class ClientForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=40,
        label="First Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
    )
    phone = forms.CharField(
        max_length=30,
        label="Phone",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone"}),
        validators=[RegexValidator(r'^[\d\-\(\) ]+$', 'Enter a valid phone number.')],
    )
    zip_code = forms.RegexField(
        regex=r'^\d{5}(?:[-\s]?\d{4})?$',
        error_messages={"invalid": "Enter a valid zip code (12345 or 12345-6789)."},
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Zip Code"}),
    )

    class Meta:
        model = Client
        fields = ['email', 'phone', 'address', 'city', 'state', 'zip_code']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            full_name = self.instance.full_name.split(' ', 1)
            self.fields['first_name'].initial = full_name[0] if full_name else ''
            self.fields['last_name'].initial = full_name[1] if len(full_name) > 1 else ''

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) not in (10, 11): 
            raise ValidationError("Phone number must contain 10 or 11 digits.")
        return phone
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.full_name = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            instance.save()
        return instance
# create new product form validation
class CreateProductForm(forms.ModelForm):
    product_name = forms.CharField(label='Product Name', max_length=100)
    price = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ['product_name', 'price']

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)
# create new service form
class CreateServiceForm(forms.ModelForm):
    service_name = forms.CharField(label='Product Name', max_length=100)
    amount = forms.DecimalField(label='Price', max_digits=10, decimal_places=2)

    class Meta:
        model = Service
        fields = ['service_name', 'amount']

    def __init__(self, *args, **kwargs):
        self.client = kwargs.pop('client', None)
        super().__init__(*args, **kwargs)