# blog/views.py
# views for the blog application
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article
import random

# Create your views here.
class ShowAllView(ListView):
    '''Define a view class to show all blog Articles.'''

    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'

class ArticleView(DetailView):
    '''Display a single Article.'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' # note singular article name

class RandomArticleView(DetailView):
    '''Display a random Article.'''

    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article' # note singular article name

    # methods
    def get_object(self):
        '''override the get_object method from detailview return one instance of the Article object selected at random'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article