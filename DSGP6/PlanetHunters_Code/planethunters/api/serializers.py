from rest_framework import serializers
from .models import Star, User
  
"""  
class StarSerializer(serializers.Serializer):

    star_id = serializers.CharField(max_length = 20)
    author = serializers.CharField(max_length = 20)

    def create(self, validated_data):
        return Star.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.star_id = validated_data.get('star_id', instance.star_id)
        instance.author = validated_data.get('author', instance.author)

    """
    
class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = ['id','star_id','author']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','user_name','user_pass','user_stars']
