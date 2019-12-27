from django import forms
from captcha.fields import CaptchaField



class UserForm(forms.Form):
    username = forms.CharField(label="Username", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '用户名', 'autofocus': ''}))
    password = forms.CharField(label="Password", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}))
    captcha = CaptchaField(label='Verification:')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )
    username = forms.CharField(label="Username", max_length=18, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="confirm password", max_length=20,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email=forms.EmailField(label="email",widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex=forms.ChoiceField(label='sex',choices=gender)
    captcha=CaptchaField(label='verification')