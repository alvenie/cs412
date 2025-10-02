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
    
class Post(models.Model):
    '''Encapsulates the data of a mini insta post by a user'''

    # define the data attributes of a Post object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.caption}'
    
class Photo(models.Model):
    '''Encapsulates the data of a mini insta photo associated with a post'''

    # define the data attributes of a Post object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Photo {self.pk} for Post {self.post.pk} taken at {self.timestamp}"