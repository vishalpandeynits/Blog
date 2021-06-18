from django.urls import path,include
from . import views
app_name = 'status'

urlpatterns = [
	path('',views.all_notes,name="all_notes"),
    path('create/',views.createpost,name="create"),
    path('mynotes/',views.mynotes,name="mynotes"),
    path('myaccount/',views.myaccount),
    path('delete/<int:id>',views.delete),
    path('update/<int:id>',views.update),
    path('status/<int:id>',views.read),
    path('signup/',views.signup,name="signup"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('query/',views.listpost.as_view()),
    path('queryd/<int:pk>',views.listdetails.as_view()),
    path('users/',views.userlist.as_view()),
    path('users/<str:username>',views.userdetail.as_view(),name="userdetail")

] 