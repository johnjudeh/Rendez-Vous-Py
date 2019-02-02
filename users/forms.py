from django import forms

from .models import User, Profile

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        ]
        widgets = {
            'password': forms.PasswordInput()
        }

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['interests']
        widgets = {
            'interests': forms.CheckboxSelectMultiple(
                attrs={
                    'class': 'interests__checkbox',
                    'tabindex': '0',
                }
            )
        }