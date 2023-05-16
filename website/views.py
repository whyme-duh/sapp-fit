from django.shortcuts import get_object_or_404, render, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .models import AboutAndQuote, Service, Blog, Post
from website.form import ContactForm
import datetime
from django.views.generic import DetailView

form = ContactForm()
count = 0
context = {
        'about' : AboutAndQuote.objects.all(),
        'services': Service.objects.all(),
        'blogs': Blog.objects.all(),
        'posts' : Post.objects.all(),
        'form':form,
        'count' : count,
        'date' :datetime.datetime.today().strftime("%Y")
    }

def index(request):
    count =0
    for i in Blog.objects.all():
        count += 1
        

    if (request.method == "GET"):
        form = ContactForm()

   
    if (request.method == "POST"):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message =form.cleaned_data['message']
            try:
                send_mail(subject, message, email, ['ritikshrestha94@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid!")
    return render(request, 'website/index.html', context)



def BlogDetailView(request, slug):
    # to fetch the logo detail
    about = AboutAndQuote.objects.all()
    blogs = Blog.objects.filter(slug=slug)
    related_blogs = Blog.objects.filter().exclude(slug=slug) 
    return render(request, 'website/blogdetail.html', {'blogs' : blogs, 'related_blogs' : related_blogs,'about' : about})


def BlogPostView(request):
    return render(request,'website/blogs.html',  context)

    

def PostView(request):
    return render(request,'website/posts.html',  context)
