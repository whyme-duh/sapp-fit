from django.contrib import admin
from . models import AboutAndQuote, Service, Blog, Post,Testimonial, Client

admin.site.register(AboutAndQuote)
admin.site.register(Service)
admin.site.register(Post)
admin.site.register(Client)
admin.site.register(Testimonial)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    prepopulated_fields = {"slug": ("title",)}


