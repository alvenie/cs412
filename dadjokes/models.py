# dadjokes/models.py
# auther: Chonghao Chen (alvenie@bu.edu), 11/13/2025
# description: The models.py file specific to the dadjokes app

from django.db import models
from django.utils import timezone

class Joke(models.Model):
    '''Encapsulates the data of a Joke model'''

    text = models.TextField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text[:50] + "..."

class Picture(models.Model):
    '''Encapsulates the data of a Picture model'''
    
    image_url = models.URLField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.image_url