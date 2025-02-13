from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from catalog.models import Home, HomeImage

CustomUser = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    phone_number = forms.CharField(required=False)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['title', 'description', 'price', 'quantity', 'city', 'street', 'house_number', 'apartment_number']

        def __init__(self, *args, user=None, **kwargs):
            super().__init__(*args, **kwargs)

            if user and not user.is_staff:
                self.fields.pop("original_address", None)

class HomeImageForm(forms.ModelForm):
    class Meta:
        model = HomeImage
        fields = ['image']
