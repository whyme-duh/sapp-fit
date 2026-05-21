from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from .models import AboutAndQuote, Booking, Client, Service, Blog, Post, Testimonial
from django.contrib.auth.decorators import login_required
from  django.contrib import messages 
import datetime
from django.views.generic import DetailView

count = 0
context = {
        'about' : AboutAndQuote.objects.all(),
        'services': Service.objects.all(),
        'blogs': Blog.objects.all(),
        'posts' : Post.objects.all(),
        'count' : count,
        'date' :datetime.datetime.today().strftime("%Y"),
        'testimonials' : Testimonial.objects.all()
    }

def index(request):
    return render(request, 'website/home.html', context)



def service_detail_view(request, slug):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            service_type = Service.objects.get(slug = slug)
            preferred_date = form.cleaned_data['preferred_date']
            phone_number = form.cleaned_data['phone_number']
            Booking.objects.create(
                name = name,
                email = email,
                phone_number = phone_number,
                service = service_type,
                preferred_date = preferred_date,
            )
            messages.success(request, f'Your booking request has been sent! We will contact you soon.')
            return redirect('service-detail', slug = slug)
        else:
            messages.error(request, f'Error occured. Try again!')
    else:
        form = BookingForm()
    service = Service.objects.get(slug = slug)
    other_services = Service.objects.all().exclude(slug = slug)
    logo = AboutAndQuote.objects.all().first()
    return render(request, 'website/service.html', context = {'service' : service, 'logo' : logo.logo, "other_services" : other_services, 'form' : form})



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


from .form import BookingForm, ClientForm

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



