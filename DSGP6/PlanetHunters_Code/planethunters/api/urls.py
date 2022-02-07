
from django.urls import path
from .views import StarDetails,StarList,UserDetails,UserList

urlpatterns = [
    path('stars/', StarList.as_view()),
    path('stars/<str:id>/', StarDetails.as_view()),
    path('users/', UserList.as_view()),
    path('users/<str:id>/', UserDetails.as_view()),
    #path('stars/', star_list),
    #path('stars/<str:pk>/', star_details),
]