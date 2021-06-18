from django.contrib.auth.models import User
from rest_framework import  serializers
from .models import Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password',)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'