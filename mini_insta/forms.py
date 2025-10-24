# mini_insta/forms.py
# auther: Chonghao Chen (alvenie@bu.edu), 10/03/2025
# define the forms that we use for create/update/delete operations

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''A form to add a post to the database'''

    # Add a non-model field for the photo's URL 
    # Make it not required to allow posts without images.
    # image_url = forms.URLField(label='Image URL', required=False)

    class Meta:
        '''Associate this form with a model from our database'''
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a profile'''

    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        fields = ['username', 'profile_image_url', 'bio_text']

class CreateProfileForm(forms.ModelForm):
    '''A form to create a profile'''

    profile_image_url = forms.URLField(required=False, label="Profile Image URL")

    class Meta:
        '''Associate this form with a model from our database'''
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']