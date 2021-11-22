from django import forms
from django.contrib.auth.hashers import make_password

from .models import Author

class RegisterForm(forms.ModelForm):
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    
    def save(self, commit=True):
        instance = super(RegisterForm, self).save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Author
        fields = ('email',  'password')


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class ResetPassword(forms.Form):
    email = forms.EmailField()

class NewPassword(forms.Form):
    old_password = forms.CharField()
    new_password = forms.CharField()