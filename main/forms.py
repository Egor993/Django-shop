#3) Меняет форму готовых форм?
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Reviews


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label="Username", help_text ="• Введите уникальное имя пользователя", widget=forms.TextInput(attrs={"class":"form-control"}))
	password1 = forms.CharField(label="Password", help_text ="• Пароль должен быть из 8 символов и не должен состоять только из цифр", widget=forms.PasswordInput(attrs={"class":"form-control"}))
	password2 = forms.CharField(label="Password Confirm", widget=forms.PasswordInput(attrs={"class":"form-control"}))
	email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={"class":"form-control"}))
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

class UserLoginForm(AuthenticationForm):
	username = forms.CharField(label="Username", widget=forms.TextInput(attrs={"class":"form-control"}))
	password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"class":"form-control"}))

class ReviewForm(forms.ModelForm):
	class Meta: # указываем от какой модели строить форму
		model = Reviews
		fields = ("name", "email", "text")


class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


