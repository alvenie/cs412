# mini_insta/views.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The views.py file specific to the mini insta app

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm
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

class UpdateProfileView(UpdateView):
    '''A view to handle updating a user's profile.'''

    # The form to use for this view
    form_class = UpdateProfileForm
    
    # The model this view will update
    model = Profile
    
    # The template to render the form
    template_name = "mini_insta/update_profile_form.html"

    def get_success_url(self):
        '''Define where to redirect after a successful form submission.'''
        
        # Get the primary key of the profile being updated
        pk = self.kwargs['pk']
        
        # Reverse the URL pattern for the profile detail page
        return reverse('show_profile', kwargs={'pk': pk})
    
class DeletePostView(DeleteView):
    """A view to handle deleting a post."""
    
    # The model this view will operate on
    model = Post
    
    # The template to render for confirmation
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        """Pass the post and profile objects to the template."""
        context = super().get_context_data(**kwargs)
        # self.object is the Post instance that the view is operating on
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        """Redirect to the user's profile page after deleting a post."""
        # Get the profile associated with the post that was just deleted
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})
    
class UpdatePostView(UpdateView):
    """A view to handle updating a post."""
    
    # The model this view will operate on
    model = Post
    
    # The template to render the update form
    template_name = "mini_insta/update_post_form.html"
    
    # Specify which fields from the Post model can be edited
    fields = ['caption']

    def get_success_url(self):
        """Redirect to the post's detail page after a successful update."""
        return reverse('show_post', kwargs={'pk': self.object.pk})