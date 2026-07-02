from django.contrib import admin
from django.urls import path
from website.views import ai_response, client_view, client_form, custom_service_request, delete_client, gemini_response, index, BlogPostView, BlogDetailView, service_book_now, service_detail_view, edit_client, services

urlpatterns = [
    path('', index, name ="home-page"),
    path('services/', services, name ="services-page"),
    path('services/<slug:slug>/', service_detail_view, name ="service-detail"),
    path('book-now/', service_book_now, name ="service-book-now"),
    path('custom-service/', custom_service_request, name ="custom-service"),
    path('ai-response/', ai_response, name ="ai-response"),
    path('blogs/', BlogPostView, name='blogs'),  
    path('blogs/<slug:slug>/', BlogDetailView, name='blog-detail'),
    path('clients/', client_view, name='client-view'),
    path('delete/<int:id>', delete_client, name='delete-client'),
    path('clients/<int:id>/edit/', edit_client, name='edit-client'),
    path('clientform/', client_form, name='client-form'),
]