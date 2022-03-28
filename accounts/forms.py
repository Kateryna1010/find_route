from django.contrib.auth import get_user_model, authenticate
from django import forms
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form_control',
                                                                               'placeholder': 'Input username'}))
    password = forms.CharField(label='Username', widget=forms.PasswordInput(attrs={'class': 'form_control',
                                                                                   'placeholder': 'Input password'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            qs = User.objects.filter(username=username)
            if not qs.exists():
                raise forms.ValidationError('User doesn`t exist')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Invalid password')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User not active')
        return super().clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form_control',
                                                                               'placeholder': 'Input username'}))
    password = forms.CharField(label='Username', widget=forms.PasswordInput(attrs={'class': 'form_control',
                                                                                   'placeholder': 'Input password'}))
    password2 = forms.CharField(label='Username', widget=forms.PasswordInput(attrs={'class': 'form_control',
                                                                                    'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords don`t match')
        return data['password2']

