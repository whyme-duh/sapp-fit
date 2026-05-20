from django.contrib import admin
from django.urls import path
from website.views import client_view, delete_client, index, BlogPostView, BlogDetailView, PostView, service_detail_view, edit_client

urlpatterns = [
    path('', index, name ="home-page"),
    path('services/<slug:slug>/', service_detail_view, name ="service-detail"),
    path('blogs/', BlogPostView, name='blogs'),
    path('posts/', PostView, name='posts'),
    path('blogs/<slug:slug>/', BlogDetailView, name='blog-detail'),
    path('clients/', client_view, name='client-view'),
    path('delete/<int:id>', delete_client, name='delete-client'),
    path('clients/<int:id>/edit/', edit_client, name='edit-client'),
]
