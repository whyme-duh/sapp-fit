from django.contrib import admin
from . models import AboutAndQuote, Booking, CustomService, Service, Blog, ServiceFeatureItem,Testimonial, Client

admin.site.register(AboutAndQuote)
admin.site.register(ServiceFeatureItem)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ('feature',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'preferred_date')
    list_filter = ('service', 'preferred_date', 'email')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):  
    list_display = ('user_name', 'user_category')
    list_filter = ('user_category',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):   
    list_display = ('name', 'gender', 'started_training_from', 'status')
    list_filter = ('services', 'status',)


@admin.register(CustomService)
class CustomServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'email','goal_choices')