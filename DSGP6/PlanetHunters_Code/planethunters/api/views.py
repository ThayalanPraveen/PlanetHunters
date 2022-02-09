import imp
import lightkurve as lk
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Star,User
from .serializers import StarSerializer, UserSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
import numpy as np


# Create your views here.

## API view to show list of stars
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

## API view to show details of a specific star
class StarDetails(APIView):
    
    ## valid function to find if star is valid
    def valid_star(self,target_name,target_author):
        try:
            search_result = lk.search_lightcurve(target_name, author=target_author)
            try:
                target = search_result.target_name
                return True
            except:
                return False
        except:
            return False

    def get_object(self,id):
        try:
            star = Star.objects.get(id = id)
            star.valid = self.valid_star(star.star_id,star.author)
            return star
        except Star.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        
    def get(self,request, id): 
        star = self.get_object(id)
        star.valid = self.valid_star(star.star_id,star.author)
        serializer = StarSerializer(star)
        return Response(serializer.data)

    def put(self, request, id):
        star = self.get_object(id)
        star.valid = self.valid_star(star.star_id,star.author)
        serializer = StarSerializer(star, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        star = self.get_object(id)
        star.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

## API view to show list of users
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

## API view to show details of users
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

## Search function
def search_star(target_name,target_author):
    if target_name == '' or target_author == '':
        print("No Target Name input/ Author selected")
        return False
    else:
        search_result = lk.search_lightcurve(target_name, author=target_author)
        filtered = False
        return search_result , filtered , 0

## search filter function
def search_filter(identifier,value,target_name,target_author):
        search_result = lk.search_lightcurve(target_name, author=target_author)
        
        if identifier == '' or value == '':
            print("Please Select Identifier & Input valid Value")
            return 0,0,0
        else:
            try:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                    value = str()
                    filter = np.where(search_result.table[identifier] == value)[0]
                    filtered = True
                    return search_result , filtered , filter
                else:
                    filter = np.where(search_result.table[identifier] == int(value))[0]
                    filtered = True
                    return search_result , filtered , filter
            except:
                filter = np.where(search_result.table[identifier] == int(value))[0]
                filtered = True
                return search_result , filtered , filter

## select star function
def select_star(hash_id,search_result,filtered,filter):
    if hash_id == '':
        print("Input valid #")
        return 0,0,0
    else:
        if filtered == True:
            lc = search_result[filter[int(hash_id)]].download()
        else:
            lc = search_result[int(hash_id)].download()
        return lc

## show search results function        
def show_search_results(search_results,filtered,filter):
    if filtered == False :
        return search_results
    else:
        return search_results[filter]           
        