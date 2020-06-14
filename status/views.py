from django.shortcuts import render,redirect
from .forms import PostForm , ProfileForm
from .models import Post ,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RegisterForm
from django.http import Http404

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
	return redirect('/status')

@login_required
def update(request,id):
	post = Post.objects.get(id = id)
	if post.user==request.user:
		form = PostForm(request.POST or None , instance = post)
		if form.is_valid():
			form.save()
			return redirect('/status')
	else:
		raise Http404()
	return render(request,'form.html',{'form':form})

def signup(request):
	if request.method=='POST':
		form= RegisterForm(request.POST, request.FILES)
		if form.is_valid() :
			new_user=form.save()
			Profile.objects.create(user=new_user)
			return redirect('/accounts/login/')
	else:
		form= RegisterForm()
	return render(request,'registration/signup.html',{'form':form,'form2':ProfileForm })

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
		form = ProfileForm(instance=request.user.profile)
	params= {'form':form,}
	return render(request,'myaccount.html',params)
