from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField()
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField()
    role = forms.ChoiceField(choices=[(0, 'Default'), (1, 'Admin'), (2, 'Librarian')])


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
