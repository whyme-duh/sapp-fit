from django.db import models
from ckeditor.fields import RichTextField 
import PIL

class AboutAndQuote(models.Model):
    bio = models.TextField()
    backgroundImage = models.ImageField(upload_to='images/bg', null=True)
    profileImage = models.ImageField(upload_to='images/bg', null=True)
    quotes = models.CharField(max_length=150)
    logo = models.FileField(upload_to='images/icon')
    facebook = models.URLField(null=True)
    instagram = models.URLField(null=True)
    pinterest = models.URLField(null=True)
    youtube = models.URLField(null=True)

    def __str__(self):
        return self.bio

   


class Service(models.Model):
    title = models.CharField(max_length=80)
    detail = models.CharField(max_length=80)
    price= models.IntegerField()
    icon = models.ImageField(upload_to='images/pics')


    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=80)
    content = RichTextField()
    thumbnail = models.ImageField(upload_to='images/thumbnails')
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null = True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=80)
    content = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='images/thumbnails')
    link = models.URLField()

    def __str__(self):
        return self.title
    


class Testimonial(models.Model):
    testimonial = models.CharField(max_length=150)
    user_name = models.CharField(max_length=80)
    user_img = models.ImageField(upload_to='images/testimonial')


    def __str__(self) -> str:
        return self.user_name