from django.contrib import admin
from . models import AboutAndQuote, Service, Blog, Post

admin.site.register(AboutAndQuote)
admin.site.register(Service)
admin.site.register(Post)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    prepopulated_fields = {"slug": ("title",)}


