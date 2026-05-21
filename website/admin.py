from django.contrib import admin
from . models import AboutAndQuote, Booking, Service, Blog, Post, ServiceFeatureItem,Testimonial, Client

admin.site.register(AboutAndQuote)
admin.site.register(Post)
admin.site.register(Client)
admin.site.register(Testimonial)
admin.site.register(ServiceFeatureItem)
admin.site.register(Booking)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('feature',)


