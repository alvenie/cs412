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
    
    def get_all_posts(self):
        '''Returns a QuerySet of posts by this profile'''

        # filter post objects by their profile and order them by timestamp in descending order
        posts = Post.objects.filter(profile = self).order_by('-timestamp') 
        return posts
    
class Post(models.Model):
    '''Encapsulates the data of a mini insta post by a user'''

    # define the data attributes of a Post object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.caption}'
    
    def get_all_photos(self):
        '''Returns a QuerySet of photos associated with this post'''

        photos = self.photo_set.all()
        return photos

class Photo(models.Model):
    '''Encapsulates the data of a mini insta photo associated with a post'''

    # define the data attributes of a Post object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        
        # REVISED __str__ METHOD
        if self.image_file:
            source = f"File: {self.image_file.name}"
        elif self.image_url:
            source = f"URL: {self.image_url}"
        else:
            source = "No Image"

        return f"Photo {self.pk} for Post {self.post.pk} taken at {self.timestamp} | Source: {source}"

    def get_image_url(self):
        '''Returns the URL to the image'''

        if self.image_file:
            return self.image_file
        
        if self.image_url:
            return self.image_url
        
        return 'https://i.postimg.cc/9Q2RqNVW/no-img-avail.jpg'
