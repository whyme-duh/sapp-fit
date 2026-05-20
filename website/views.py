from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .models import AboutAndQuote, Client, Service, Blog, Post, Testimonial
from website.form import ContactForm
from django.contrib.auth.decorators import login_required
from  django.contrib import messages 
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
        'date' :datetime.datetime.today().strftime("%Y"),
        'testimonials' : Testimonial.objects.all()
    }

def index(request):
    count =0
    for i in Blog.objects.all():
        count += 1
        

    if request.method == "GET":
        form = ContactForm()

   
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message =form.cleaned_data['message']
            try:
                send_mail(subject, message, email, ['ritikshrestha94@gmail.com'], fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid!")
    return render(request, 'website/home.html', context)



def service_detail_view(request, slug):
    service = Service.objects.get(slug = slug)
    other_services = Service.objects.all().exclude(slug = slug)
    logo = AboutAndQuote.objects.all().first()
    return render(request, 'website/service.html', context = {'service' : service, 'logo' : logo.logo, "other_services" : other_services})



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


from .form import ClientForm

@login_required
def client_view(request):
    if not request.user.is_superuser:
        return redirect('home-page')
    
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'New client succesfully added!')
            return redirect('client-view')
        else:
            messages.error(request, f'Error occured. Try again!')
    else:
        form = ClientForm()
    active_clients_count = Client.objects.filter(status = "Ongoing").count()
    about = AboutAndQuote.objects.all()
    clients = Client.objects.all()
    return render(request, 'website/clients/clients.html', {'clients' : clients, 'about' : about, "active_clients_count": active_clients_count, 'form': form})


@login_required
def delete_client(request, id):
    if not request.user.is_superuser:
        return redirect('home-page')
    try:
        Client.objects.get(id = id).delete()
        messages.success(request, f'Deleted successfully')
        return redirect('client-view')
    except:
        messages.error(request, f'Failed to Delete')
    return redirect('client-view')


@login_required
def edit_client(request, id):
    if not request.user.is_superuser:
        return redirect('home-page')
    
    client = get_object_or_404(Client, id = id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance = client)
        if form.is_valid():
            form.save()
            messages.success(request, f"{client.name}'s details updated!")
        else:
            messages.error(request, f"Failed to update the client's detail. Try again!")
    else:
        form = ClientForm()
    return redirect('client-view')
