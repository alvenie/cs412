# dadjokes/views.py
# auther: Chonghao Chen (alvenie@bu.edu), 11/13/2025
# description: The views.py file specific to the dadjokes app

import random
from django.views.generic import ListView, DetailView, TemplateView
from .models import Joke, Picture
from rest_framework import generics
from .serializers import JokeSerializer, PictureSerializer

# Regular Django Class-Based Views
class RandomJokeAndPictureView(TemplateView):
    '''
    Display one random Joke and one random Picture.
    This view is more flexible than DetailView for showing
    multiple, unrelated objects.
    '''

    template_name = 'dadjokes/random.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get random joke
        jokes = list(Joke.objects.all())
        context['joke'] = random.choice(jokes) if jokes else None
        
        # Get random picture
        pictures = list(Picture.objects.all())
        context['picture'] = random.choice(pictures) if pictures else None
        
        return context

class AllJokesView(ListView):
    '''Display a list of all Jokes.'''

    model = Joke
    template_name = 'dadjokes/all_jokes.html'
    context_object_name = 'jokes'

class JokeDetailView(DetailView):
    '''Display a single Joke by its primary key.'''

    model = Joke
    template_name = 'dadjokes/joke_detail.html'
    context_object_name = 'joke'

class AllPicturesView(ListView):
    '''Display a list of all Pictures.'''

    model = Picture
    template_name = 'dadjokes/all_pictures.html'
    context_object_name = 'pictures'

class PictureDetailView(DetailView):
    '''Display a single Picture by its primary key.'''

    model = Picture
    template_name = 'dadjokes/picture_detail.html'
    context_object_name = 'picture'

# Generic API Views
class ApiJokeList(generics.ListCreateAPIView):
    '''
    API view to list all jokes (GET) or create a new joke (POST).
    This follows the 'ArticleListAPIView' example.
    Handles 'api/jokes/'
    '''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class ApiJokeDetail(generics.RetrieveAPIView):
    '''
    API view to retrieve a single joke by pk (GET).
    Handles 'api/joke/<int:pk>/'
    '''

    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class ApiPictureList(generics.ListAPIView):
    '''
    API view to list all pictures (GET).
    Handles 'api/pictures/'
    '''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class ApiPictureDetail(generics.RetrieveAPIView):
    '''
    API view to retrieve a single picture by pk (GET).
    Handles 'api/picture/<int:pk>/'
    '''

    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class ApiRandomJoke(generics.RetrieveAPIView):
    '''
    API view to retrieve a random joke (GET).
    We override get_object, similar to your RandomArticleView example.
    Handles 'api/' and 'api/random/'
    '''

    serializer_class = JokeSerializer

    def get_object(self):
        '''Override to return a random Joke instance.'''
        jokes = list(Joke.objects.all())
        if jokes:
            return random.choice(jokes)
        return None # DRF will handle this as a 404

class ApiRandomPicture(generics.RetrieveAPIView):
    '''
    API view to retrieve a random picture (GET).
    Handles 'api/random_picture/'
    '''
    
    serializer_class = PictureSerializer

    def get_object(self):
        '''Override to return a random Picture instance.'''
        pictures = list(Picture.objects.all())
        if pictures:
            return random.choice(pictures)
        return None