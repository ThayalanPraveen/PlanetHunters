from rest_framework import serializers
from .models import Star, User

class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ['id','star_id','author','valid']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','user_name','user_pass','user_stars']
