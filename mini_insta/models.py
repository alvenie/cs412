# mini_insta/models.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The models.py file specific to the mini insta app

from django.db import models

# Create your models here.

class Profile(models.Model):
    '''Encapsulates the data of a mini insta Profile by a user'''
    
    # define the data attributes of a Profile object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.display_name}'