from django.db import models
from ckeditor.fields import RichTextField 

class AboutAndQuote(models.Model):
    bio = models.TextField()
    phone_number = models.IntegerField(default= 9812312312)
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
    tag = models.CharField(max_length=100, null = True, blank = True, help_text="Add a comma after each tag and make sure it is less than 5.")

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
    
class Blog(models.Model):
    title = models.CharField(max_length=80)
    content = RichTextField()
    thumbnail = models.ImageField(upload_to='images/thumbnails')
    date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null = True)

    def __str__(self):
        return self.title

    def total_time_to_read(self):
        """
        this function helps to calculate the total time to read the blog
        based on the number of words present along with average reading speed.
        """
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

    PAID_OPTIONS = [
        ("Paid", "Paid"),
        ("Not Paid", "Not Paid"),
        ("Half Paid", "Half Paid"),
    ]

    name = models.CharField(max_length=100)
    total_sessions = models.IntegerField(default = 1)
    age = models.IntegerField()
    gender = models.TextField(choices= GENDER_CHOICES)
    started_training_from = models.DateField()
    services = models.ForeignKey(Service, on_delete= models.PROTECT)
    any_problem = models.CharField(max_length=500, default="N/A")
    status = models.CharField(max_length = 100, choices= STATUS_CHOICES, default="Ongoing")
    paid_or_not = models.CharField(max_length = 100, choices= PAID_OPTIONS, blank = True, null = True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.total_sessions == 0:
            self.status = "Completed"
        if self.status == "Completed":
            self.total_sessions = 0
        super().save(*args, **kwargs)
    
class Booking(models.Model):
    status_choices = [
        ("Pending" , "Pending"),    
        ("Confirmed" , "Confirmed"),
        ("Cancelled" , "Cancelled") ]
   
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField(
        max_length=10,
    )
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    message = models.TextField(blank=True)
    preferred_date = models.DateField() 
    status = models.CharField(max_length=20, choices=status_choices, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.service.title}'

class CustomService(models.Model):

    GOAL_CHOICES = [
        ("Fat Loss & Toning" , "Fat Loss & Toning"),    
        ("Building Muscle & Strength" , "Building Muscle & Strength"),
        ("General Health & Mobility" , "General Health & Mobility"),
        ("Rehabilitation" , "Rehabilitation"),
        ("HYROX / Event Prep", "HYROX / Event Prep"),
        ("Other" , "Other")
    ]

    PLAN_DURATION_OPTIONS = [
        ("1 Week Plan", "1 Week Plan"),
        ("4 Weeks Plan", "4 Weeks Plan"),
        ("12 Weeks Plan", "12 Weeks Plan"),
    ]

    WORKOUT_TIME_OPTIONS = [
        ("30 minutes", "30 minutes"),
        ("45 minutes", "45 minutes"),
        ("1 hour", "1 hour"),
    ]

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ("Sedentary", "Sedentary (little or no exercise)"),
        ("Lightly Active", "Lightly Active (light exercise/sports 1-3 days/week)"),
        ("Moderately Active", "Moderately Active (moderate exercise/sports 3-5 days/week)"),
        ("Very Active", "Very Active (hard exercise/sports 6-7 days a week)"),
        ("Super Active", "Super Active (very hard exercise/sports & physical job or 2x training)"),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField(blank = True, null = True)
    weight = models.IntegerField(blank = True, null = True)
    gender = models.TextField(choices= Client.GENDER_CHOICES, blank = True)
    activity_level = models.TextField(choices= ACTIVITY_LEVEL_CHOICES, blank = True)
    email = models.EmailField()
    phone_number = models.IntegerField()
    goal_choices = models.CharField(max_length=200, choices = GOAL_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    special_notes = models.TextField(blank=True)
    equipment_used = models.TextField(blank=True)
    preferred_duration = models.CharField(max_length=20, choices=PLAN_DURATION_OPTIONS, blank=True)
    workout_time = models.CharField(max_length=20, choices=WORKOUT_TIME_OPTIONS, blank=True)

    def __str__(self):
        return f'{self.name} - Custom Service Request'
    