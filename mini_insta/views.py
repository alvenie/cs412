# mini_insta/views.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The views.py file specific to the mini insta app

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm
from django.urls import reverse

# Create your views here.

class ProfileListView(ListView):
    '''Define a view class to show all mini insta Profiles.'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Define a view class to show a specific Profile'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''Define a view class to show a specific Post'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    '''A view to handle creation of a post on a profile'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Post.'''

        # Redirect back to the profile page, not an 'article' page
        return reverse('show_post', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        '''Passes the parent Profile object to the template.'''

        # Get the default context
        context = super().get_context_data(**kwargs)

        # Get the Profile object using the pk from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # Add the profile to the context dictionary
        context['profile'] = profile

        return context

    def form_valid(self, form):
        '''Links the new Post to the correct Profile before saving.'''

        # Get the Profile object from the URL's pk
        #profile = Profile.objects.get(pk=self.kwargs['pk'])

        # Assign this profile to the new post's profile field
        #form.instance.profile = profile

        # Let the parent class save the object
        #response = super().form_valid(form)

        #image_url = form.cleaned_data.get('image_url')

        #if image_url:
        #    Photo.objects.create(
        #        post = self.object,
        #        image_url = image_url
        #    )
        
        # Assign the profile to the new post object before saving the form.
        # The profile's pk is retrieved from the URL.
        form.instance.profile = Profile.objects.get(pk=self.kwargs['pk'])

        # Let the parent CreateView's form_valid method save the Post.
        # This sets self.object to the newly created post instance.
        response = super().form_valid(form)

        # Retrieve the list of uploaded files from the request.
        uploaded_images = self.request.FILES.getlist('images')

        # Loop through the uploaded files and create a Photo object for each one.
        for image_file in uploaded_images:
            Photo.objects.create(post=self.object, image_file=image_file)

        # Return the HttpResponseRedirect object.
        return response
