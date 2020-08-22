from django import forms
import django
from django.forms import ModelForm
from .models import Post, Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
	class Meta(ModelForm):
		model = Post
		exclude =('date_pub','author','user')

class ProfileForm(forms.ModelForm):
	class Meta(ModelForm):
		model = Profile
		exclude = ('user',)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    #you can add first name,last name, full name , email input fields here,
    #if you still not satisfied with these fields, you have to make one more
    #model , and  associate a form with it and render this form with user registration
    class Meta:
        model = User
        fields = ("username","email",'password1','password2',)
