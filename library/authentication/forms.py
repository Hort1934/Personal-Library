from django import forms
from .models import CustomUser

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    # middle_name = forms.CharField(required=False)
    last_name = forms.CharField()
    # role = forms.ChoiceField(choices=[(0, 'Visitor'), (1, 'Librarian')])
#     test


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email']





