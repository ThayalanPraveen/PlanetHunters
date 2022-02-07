
from django.urls import path
from .views import StarDetails,StarList

urlpatterns = [
    path('stars/', StarList.as_view()),
    path('stars/<str:id>/', StarDetails.as_view()),
    #path('stars/', star_list),
    #path('stars/<str:pk>/', star_details),
]