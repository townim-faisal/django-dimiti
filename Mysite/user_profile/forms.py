from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm
from .models import Profile

class ProfileForm(ModelForm):
    #email = forms.EmailField(label="Email", max_length=200, help_text='Required')
    #password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
    #password2 = forms.CharField(label="Password Confirmation",widget=forms.PasswordInput)
    profile_image = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'avatar_url', 'avatar_path']
        widgets = {
            'birth_date': AdminDateWidget(),
        }
