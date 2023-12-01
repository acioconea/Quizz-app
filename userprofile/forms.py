from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import TextInput


class NewAccountForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

        widgets = {
            "first_name": TextInput(attrs={"placeholder": "First name", "class": "form-control"}),
            "last_name": TextInput(attrs={"placeholder": "Last name", "class": "form-control"}),
            "email": TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
            "username": TextInput(attrs={"placeholder": "Username", "class": "form-control"}),
            "password1": TextInput(attrs={"placeholder": "Password", "class": "form-control", "type": "password"}),
            "password2": TextInput(
                attrs={"placeholder": "Confirm password", "class": "form-control", "type": "password"}),
        }

    def __init__(self, pk, *args, **kwargs):
        super(NewAccountForm, self).__init__(*args, **kwargs)
        self.pk = pk

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Usernameul deja exista! Te rugam sa alegi alte valori")
        return username


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
