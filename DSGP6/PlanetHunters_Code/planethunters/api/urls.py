
from django.urls import path
from .views import StarDetails,StarList,UserDetails,UserList

urlpatterns = [
    path('stars/', StarList.as_view()),
    path('stars/<int:id>/', StarDetails.as_view()),
    path('users/', UserList.as_view()),
    path('users/<str:id>/', UserDetails.as_view()),
    ##path('home/',home.html) 
]

"""  
For Website

https://www.srilankanplanethunters.com/home
https://www.srilankanplanethunters.com/about
https://www.srilankanplanethunters.com/features
https://www.srilankanplanethunters.com/blog

For dashboard

dashboard/home
dashboard/search
dashboard/filter
dashboard/analyze
dashboard/machinelearning
dashboard/habitability
dashboard/profile
dashboard/signin
dashboard/register
dashboard/forgetpwd
"""

