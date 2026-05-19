from django.contrib import admin
from django.urls import path
from website.views import client_view, index, BlogPostView, BlogDetailView, PostView, service_detail_view

urlpatterns = [
    path('', index, name ="home-page"),
    path('services/<slug:slug>/', service_detail_view, name ="service-detail"),
    path('blogs/', BlogPostView, name='blogs'),
    path('posts/', PostView, name='posts'),
    path('blogs/<slug:slug>/', BlogDetailView, name='blog-detail'),
    path('clients/', client_view, name='client-view'),
]
