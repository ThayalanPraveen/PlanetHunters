
from django.urls import path
from .views import StarDetails,StarList,UserDetails,UserList

urlpatterns = [
    path('stars/', StarList.as_view()),
    path('stars/<int:id>/', StarDetails.as_view()),
    path('users/', UserList.as_view()),
    path('users/<str:id>/', UserDetails.as_view()),
]