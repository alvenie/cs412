# mini_insta/urls.py
# auther: Chonghao Chen (alvenie@bu.edu), 9/25/2025
# description: The urls.py file specific to the mini insta app
# define URL patterns for the blog application

from django.urls import path
from .views import * 
# ProfileListView, ProfileDetailView, PostDetailView, UpdateProfileView, DeletePostView, UpdatePostView, ShowFollowersDetailView, ShowFollowingDetailView, CreateProfileView, LogoutConfirmationView, PostFeedListView, SearchView, CreatePostView

# generic view for authentication/authorization
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='show_post'),
    path('profile/create_post', CreatePostView.as_view(), name='create_post_form'),
    path('profile/update', UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', UpdatePostView.as_view(), name='update_post'),
    path('profile/<int:pk>/followers', ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/feed', PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', SearchView.as_view(), name='search'),

    ## Like/Unlike urls
    path('post/<int:pk>/like/', AddLikeView.as_view(), name='like'),
    path('post/<int:pk>/delete_like/', DeleteLikeView.as_view(), name='unlike'),

    ## Follow/Unfollow urls
    path('profile/<int:pk>/follow/', AddFollowView.as_view(), name='follow'),
    path('profile/<int:pk>/delete_follow/', DeleteFollowView.as_view(), name='unfollow'),

    ## authorization related urls
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
]
