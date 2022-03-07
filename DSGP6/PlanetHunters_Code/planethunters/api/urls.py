
from django import views
from django.urls import path
from .views import StarDetails,StarList,UserDetails,UserList

urlpatterns = [
    path('stars/', StarList.as_view()),
    path('home/', views.home),
    path('stars/<int:id>/', StarDetails.as_view()),
    path('users/', UserList.as_view()),
    path('users/<str:id>/', UserDetails.as_view()),
    ##path('home/',home.html) 
    ##path('about/', about.html)
    ##path('features/',features.html)
    ##path('blog/',blog.html)
    
    ##path('dashboard/home/',home.html)
    ##path('dashboard/search/',search.html)
    ##path('dashboard/filter/',filter.html)
    ##path('dashboard/analyze/',analyze.html)
    ##path('dashboard/machinelearning/',machinelearning.html)
    ##path('dashboard/habitability/',habitability.html)
    ##path('dashboard/profile/',profile.html)
    ##path('dashboard/signin/',signin.html)
    ##path('dashboard/register/',register.html)
    ##path('dashboard/forgetpwd/',forgetpwd.html)

]