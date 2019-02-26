from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    #email = forms.EmailField(label="Email", max_length=200, help_text='Required')
    #password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    #password2 = forms.CharField(label="Password Confirmation",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

    def clean_password2(self):
        cleanData = self.cleaned_data
        if cleanData['password1'] != cleanData['password2']:
            raise forms.ValidationError("Password didn't match")
        else:
            return cleanData['password2']
