from django import forms
from .models import CropListing, User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    is_seller = forms.BooleanField(required=False, label="Register as Seller")
    is_customer = forms.BooleanField(required=False, label="Register as Customer")

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2', 'is_seller', 'is_customer']

    def clean(self):
        cleaned_data = super().clean()
        is_seller = cleaned_data.get('is_seller')
        is_customer = cleaned_data.get('is_customer')
        if not is_seller and not is_customer:
            raise forms.ValidationError("You must select at least one role.")
        return cleaned_data

class CropListingForm(forms.ModelForm):
    class Meta:
        model = CropListing
        fields = ['crop_name', 'variety', 'quantity', 'expected_price', 'image']