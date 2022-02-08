import imp
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Star,User
from .serializers import StarSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView


# Create your views here.

class StarList(APIView):
    def get(self, request):
        stars = Star.objects.all()
        serializer = StarSerializer(stars , many =True)
        return Response(serializer.data)

    def post(self,request):
        serializer = StarSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class StarDetails(APIView):
    def get_object(self,id):
        try:
            star = Star.objects.get(star_id = id)
            return star
        except Star.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
    def get(self,request, id): 
        star = self.get_object(id)
        serializer = StarSerializer(star)
        return Response(serializer.data)

    def put(self, request, id):
        star = self.get_object(id)
        serializer = StarSerializer(star, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        star = self.get_object(id)
        star.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class UserList(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users , many =True)
        return Response(serializer.data)

    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserDetails(APIView):
    def get_object(self,id):
        try:
            user = User.objects.get(user_name = id)
            return user
        except Star.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
    def get(self,request, id): 
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = self.get_object(id)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        user = self.get_object(id)
        user.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

# vs code push test