from django import forms
from django.contrib.auth.models import User
from .models import Contact, Orders

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']

class CheckoutForm(forms.ModelForm):
    paymentMethod = forms.ChoiceField(choices=[('cod', 'Cash on Delivery'), ('paytm', 'PayTm')], required=True)
    itemsJson = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Orders
        fields = ['amount', 'name', 'email', 'address', 'city', 'state', 'zip_code', 'phone']

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    role = forms.ChoiceField(choices=[('SELLER', 'Seller'), ('CUSTOMER', 'Customer')], initial='CUSTOMER')
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
