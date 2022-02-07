import imp
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Star
from .serializers import StarSerializer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView


# Create your views here.
'''
@api_view(["GET","POST"])
def star_list(request):
    if request.method == "GET":
        stars = Star.objects.all()
        serializer = StarSerializer(stars , many =True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = StarSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
def star_details(request, pk):
    try:
        star = Star.objects.get(star_id = pk)
    except Star.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = StarSerializer(star)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = StarSerializer(star, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE" :
        star.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
'''


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
