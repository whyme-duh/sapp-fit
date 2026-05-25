from django.db import models
from ckeditor.fields import RichTextField 
import PIL

class AboutAndQuote(models.Model):
    bio = models.TextField()
    phone_number = models.IntegerField(default= 98123123122, max_length = 10)
    email_id = models.EmailField(blank = True)
    backgroundImage = models.ImageField(upload_to='images/bg', null=True)
    profileImage = models.ImageField(upload_to='images/bg', null=True)
    quoteContainerImage = models.ImageField(upload_to='images/bg', null=True)
    quotes = models.CharField(max_length=150)
    logo = models.FileField(upload_to='images/icon')
    facebook = models.URLField(null=True)
    instagram = models.URLField(null=True)
    pinterest = models.URLField(null=True)
    youtube = models.URLField(null=True)

    def __str__(self):
        return self.bio
    

    

class ServiceFeatureItem(models.Model):
    service_item = models.TextField(null = True)

    def __str__(self):
        return self.service_item


class Service(models.Model):
    title = models.CharField(max_length=80)
    info = models.TextField(null = True, blank = True)
    feature = models.ManyToManyField(ServiceFeatureItem, blank = True, related_name="services")
    price= models.IntegerField()
    icon = models.ImageField(upload_to='images/pics')
    slug = models.SlugField(null = True)


    def __str__(self):
        return f'{self.title} (Rs. {self.price})'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.thumbnail.path)
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)
    




class Blog(models.Model):
    title = models.CharField(max_length=80)
    content = RichTextField()
    thumbnail = models.ImageField(upload_to='images/thumbnails')
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null = True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = PIL.Image.open(self.thumbnail.path)
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)

    def total_time_to_read(self):
        return len(self.content.split()) // 200



class Testimonial(models.Model):
    testimonial = models.CharField(max_length=150)
    user_name = models.CharField(max_length=80)
    user_category = models.CharField(max_length=80, default="A member")

    def __str__(self) -> str:
        return self.user_name
    


class Client(models.Model):

    GENDER_CHOICES = [
        ("Male" , "Male"),
        ("Female", "Female"),
        ("Other" , "Other")
    ]

    STATUS_CHOICES = [
        ("Ongoing" , "Ongoing"),
        ("Completed", "Completed"),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.TextField(choices= GENDER_CHOICES)
    started_training_from = models.DateField()
    services = models.ForeignKey(Service, on_delete= models.PROTECT)
    any_problem = models.TextField(default="N/A")
    status = models.TextField(choices= STATUS_CHOICES)

    def __str__(self):
        return self.name


class Booking(models.Model):

    status_choices = [
        ("Pending" , "Pending"),    
        ("Confirmed" , "Confirmed"),
        ("Cancelled" , "Cancelled") ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField( max_length = 10)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    message = models.TextField(blank=True)
    preferred_date = models.DateField() 
    status = models.CharField(max_length=20, choices=status_choices, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.name} - {self.service.title}'
    