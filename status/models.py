from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime
x=datetime.now()
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
	picture= models.ImageField(upload_to = "media/images/")
	subject = models.CharField(max_length=100)
	title=models.CharField(max_length=100)
	content = RichTextUploadingField(blank=True)
	date_pub = models.DateField(default= x.strftime("%Y-%m-%d"),null =True)

	
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete =models.CASCADE,null=True)
	profile_pic = models.ImageField(upload_to = "media/profile_pic/",null=True, blank= True)
	location = models.CharField(max_length=100,null=True, blank= True)
	facebook_profile=models.URLField(null=True)
	twitter_profile = models.URLField(null=True)
	
