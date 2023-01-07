from django.contrib import admin
from django.urls import path
from website.views import index, BlogPostView, BlogDetailView, PostView

urlpatterns = [
    path('', index, name ="home-page"),
    path('blogs/', BlogPostView, name='blogs'),
    path('posts/', PostView, name='posts'),
    path('blogs/<slug:slug>/', BlogDetailView, name='blog-detail')
]
