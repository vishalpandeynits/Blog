from django.urls import path,include
from .views import *

urlpatterns = [
	path('',all_notes,name="all_notes"),
    path('signup/',signup,name="signup"),
    path('create/',createpost,name="create"),
    path('mynotes/',mynotes,name="mynotes"),
    path('myaccount/',myaccount),
    path('delete/<int:id>',delete),
    path('update/<int:id>',update),
    path('status/<int:id>',read),
    path('query/',listpost.as_view()),
    path('queryd/<int:pk>',listdetails.as_view()),
    path('users/',userlist.as_view()),
    path('users/<str:username>',userdetail.as_view(),name="userdetail")
] 