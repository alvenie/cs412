# file: blog/serializer.py
# this file explains how to convert our Django data models
# for transmission as text over HTTP

from rest_framework import serializers
from .models import *

class ArticleSerializer(serializers.ModelSerializer):
    '''
    A serializer class for the Article model.
    Specifies which fields are exposed in the API.
    '''

    class Meta:
        model = Article
        fields = ['id', 'title', 'text', 'author', 'published', 'image_file']

    # we can add extra code to execute on create/read/update/delete operations.
    def create(self, validated_data):
        '''hand object creation'''

        print(f'ArticleSerializer.create(), validated_data={validated_data}')
        # create an Article object and attach pk
        article = Article.objects.create(user=User.objects.first(),
                                         **validated_data)

        # save to database
        article.save()

        # return the article instance
        return article