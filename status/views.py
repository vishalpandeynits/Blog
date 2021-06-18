from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .forms import PostForm , ProfileForm
from .models import Post ,Profile
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.http import Http404

from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse, request
from .serializers import PostSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework import generics

def signup(request):
	if request.method=='POST':
		form= RegisterForm(request.POST, request.FILES)
		if form.is_valid() :
			new_user=form.save()
			Profile.objects.create(user=new_user)
			return redirect('all_notes')
	else:
		form= RegisterForm()
	return render(request,'registration/signup.html',{'form':form,'form2':ProfileForm })

@login_required
def createpost(request):
	if request.method=="POST":
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			data=form.save()
			data.user=request.user
			data.save()
			return redirect('/mynotes')
	else:
		form = PostForm()
	return render(request,'form.html',{'form':form})


def all_notes(request):
	post= Post.objects.all().order_by('-id')
	if request.GET.get('search'):
		search=request.GET.get('search')
		post=post.filter(Q(subject__icontains=search)|Q(title__icontains=search)|Q(content__icontains=search))
	params= {'post':post,
			'num_posts':len(post),
			}
	return render(request,'post.html',params)

@login_required
def delete(request,id):
	post = Post.objects.get(id=id)
	if post.user==request.user:
		post.delete()
	else:
		raise Http404()
	return redirect('all_notes')

@login_required
def update(request,id):
	post = Post.objects.get(id = id)
	if post.user==request.user:
		form = PostForm(request.POST or None , instance = post)
		if form.is_valid():
			form.save()
			return redirect(f'/status/{id}')
	else:
		raise Http404()
	return render(request,'form.html',{'form':form})

def read(request,id):
	post=Post.objects.get(id=id)
	params={'read':post}
	return render(request,'read.html',params)

@login_required
def mynotes(request):
	mynotes = Post.objects.all().filter(user=request.user).order_by('-id')
	if request.GET.get('search'):
		search=request.GET.get('search')
		mynotes=mynotes.filter(Q(subject__icontains=search)|Q(title__icontains=search)|Q(content__icontains=search))
	params= {'mynotes':mynotes}
	return render(request,'mynotes.html',params)

@login_required
def myaccount(request):
	if request.method=='POST':
		form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
		if form.is_valid():
			profile = form.save(commit= False)
			profile.user= request.user
			profile.save()
			return redirect('/myaccount')
	else:
		try:
			form = ProfileForm(instance=request.user.profile)
		except User.profile.RelatedObjectDoesNotExist:
			form = ProfileForm()
	params= {'form':form,}
	return render(request,'myaccount.html',params)

@csrf_exempt
@api_view(['GET','POST'])
def postlist(request):
	if request.method =='GET':
		queryset = Post.objects.all()
		serializer = PostSerializer(queryset, many = True)
		return Response(serializer.data)
	elif request.method =="POST":
		data = JSONParser.parse(request)
		serializer = PostSerializer(data = data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data , status = 201)
		return Response(serializer.data, status = 400)

@csrf_exempt
def postdetail(request, pk):
	try:
		post = Post.object.get(id = pk)
	except Post.DoesNotExist:
		return HttpResponse(status = 404)
	if request.method == 'GET':
		serializer = PostSerializer(post)
		return JsonResponse(serializer.data, status = 201)

	elif request.method == 'PUT':
		data = JSONParser.parse(request)
		serializer = PostSerializer(data = data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status = 201)
	elif request.method == 'DELETE':
		post.delete()
		return HttpResponse(status=204)

class PostListt(APIView):
	def get_me(self):
		return Post.objects.all()
	def get(self,request,*args,**kwargs):
		serializer = PostSerializer(self.get_me(),many=True)
		return Response(serializer.data)

	def post(self, request, *args,**kwargs):
		serializer = PostSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = 201)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
	def get_object(self, id):
		try:
			return Post.objects.get(id=id)
		except Post.DoesNotExist:
			raise Http404()

	def get(self,request,pk,*args,**kwargs):
		post = self.get_object(id = pk)
		serializer = PostSerializer(post)
		return Response(serializer.data)

	def put(self, request,pk, format=None):
		post = self.get_object(id = pk)
		serializer = PostSerializer(post, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request,pk, *args,**kwargs):
		self.get_object(id =pk).delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

## USING MIXINS 
class posts(mixins.CreateModelMixin,
			mixins.ListModelMixin,
			generics.GenericAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def create(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class postadd(mixins.UpdateModelMixin,
			mixins.DestroyModelMixin,
			mixins.RetrieveModelMixin,
			generics.GenericAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

	def get(self,request,*args,**kwargs):
		return self.retrieve(request,*args,**kwargs)
	
	def put(self, request,*args,**kwargs):
		return self.update(request,*args,**kwargs)

	def delete(self, request,*args,**kwargs):
		return self.destroy(request,*args,**kwargs)

class listpost(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class listdetails(generics.RetrieveUpdateDestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class userlist(generics.ListAPIView):
	serializer_class = UserSerializer
	def get_queryset(self,*args,**kwargs):
		return User.objects.all()

class userdetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = UserSerializer
	def get_queryset(self,*args,**kwargs):
		return User.objects.all()