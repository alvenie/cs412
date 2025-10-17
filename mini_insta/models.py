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
    
    def get_followers(self):
        '''Return a list of profiles who follow the current profile'''

        # find all follow object where it is following this profile
        follower_relations = Follow.objects.filter(profile=self)

        followers = [relation.follower_profile for relation in follower_relations]

        return followers
    
    def get_num_followers(self):
        '''Return the count of followers'''

        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        '''Return a list of profiles who the current profile follows'''

        # Find all 'Follow' objects where this profile is the follower
        follow_relations = Follow.objects.filter(follower_profile = self)

        follow = [relation.profile for relation in follow_relations]

        return follow
    
    def get_num_following(self):
        '''Return the count of follows'''

        return Follow.objects.filter(follower_profile = self).count()
    
    def get_post_feed(self):
        """Return the list of posts for the feed from profiles the user follows."""
        
        # Get the list of profiles that the current user is following.
        following_profiles = self.get_following()
        
        # Filter the Post model to get all posts where the author's profile is in the list of profiles we're following. Order by the most recent.
        post_feed = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
        
        return post_feed
    
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
    
    def get_all_comments(self):
        '''Returns a QuerySet of comments associated with this post'''

        comments = Comment.objects.filter(post = self).order_by('timestamp')
        return comments
    
    def get_likes(self):
        '''Returns all likes on a post'''

        likes = Like.objects.filter(post = self).order_by('timestamp')
        return likes

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
            return self.image_file.url
        
        if self.image_url:
            return self.image_url
        
        return 'https://i.postimg.cc/9Q2RqNVW/no-img-avail.jpg'

class Follow(models.Model):
    '''Encapsulates the data of a follow'''

    # define the data attributes of a follow object
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"{self.follower_profile.username} follows {self.profile.username}"
    
class Comment(models.Model):
    '''Encapsulates the data of a comment'''

    # define the data attributes of a comment object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True)

    def __str__(self):

        return f"{self.profile} commented on {self.post}"

class Like(models.Model):
    '''Encapsulates the data of a like'''

    # define the data attributes of a comment object
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"{self.profile} liked {self.post}"
