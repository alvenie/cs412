# dadjokes/serializers.py
# auther: Chonghao Chen (alvenie@bu.edu), 11/13/2025
# description: The serializers.py file specific to the dadjokes app

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    '''
    A serializer class for the Joke model.
    Specifies which fields are exposed in the API.
    '''

    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'created_at']

class PictureSerializer(serializers.ModelSerializer):
    '''
    A serializer class for the Picture model.
    Specifies which fields are exposed in the API.
    '''
        
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created_at']