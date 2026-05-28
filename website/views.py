import datetime
from django.shortcuts import get_object_or_404, redirect, render
import threading
from sapfit import settings
from .models import AboutAndQuote, Booking, Client, Service, Blog, Testimonial
from django.contrib.auth.decorators import login_required
from  django.contrib import messages 
from django_ratelimit.decorators import ratelimit
from .form import BookingForm, ClientForm
from django.core.mail import send_mail


context = {
    'about' : AboutAndQuote.objects.all(),
    'services': Service.objects.all(),
    'blogs': Blog.objects.all(),
    'date' :datetime.datetime.today().strftime("%Y"),
    'testimonials' : Testimonial.objects.all()
    }

def index(request):
    return render(request, 'website/home.html', context)


def send_email_about_booking(client_name, client_email, service_type, preferred_date):
    subject  = f"New Booking Request from {client_name}"
    message = f"""
    Great news! You have a new booking request.
    
    Client Name: {client_name}
    Client Email: {client_email}
    Requested Service: {service_type}
    Preferred Time: {preferred_date}
    
    Log into the SAPPFIT dashboard to approve or manage this booking.
    """
    try:
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST_USER,
            ['saprinashrestha72@gmail.com'],
            fail_silently=False,
        )
    except Exception as e:  
        print(f"Error sending email: {e}")

@ratelimit(key='ip', rate='3/h', method= 'POST', block = False)
def service_detail_view(request, slug):
    if request.method == "POST":
        was_limited = getattr(request, 'limited', False)

        if was_limited:
            messages.error(request, f'Too many booking requests from this IP. Please try again later.')
            return redirect('service-detail', slug = slug)
        
        form = BookingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            service_type = Service.objects.get(slug = slug)
            preferred_date = form.cleaned_data['preferred_date']
            phone_number = form.cleaned_data['phone_number']

            existing_booking_check = Booking.objects.filter(name = name, email = email, service = service_type, preferred_date = preferred_date).exists()
            if existing_booking_check:
                messages.error(request, f'You have already booked this service for the selected date.')
                return redirect('service-detail', slug = slug)
            else:
                Booking.objects.create(
                    name = name,
                    email = email,
                    phone_number = phone_number,
                    service = service_type,
                    preferred_date = preferred_date,
                )
                email_thread = threading.Thread(target=send_email_about_booking, args=(name, email, service_type, preferred_date))
                email_thread.start()
                messages.success(request, f'Your booking request has been sent! We will contact you soon.')
                
            return redirect('service-detail', slug = slug)
            
        else:
            error_details = form.errors.as_text()
            messages.error(request, f'Error occured. Try again! Details: {error_details}')
    else:
        form = BookingForm()
    service = Service.objects.get(slug = slug)
    other_services = Service.objects.all().exclude(slug = slug)
    about = AboutAndQuote.objects.all()
    return render(request, 'website/servicedetail.html', context = {'service' : service, 'about' : about, "other_services" : other_services, 'form' : form})



def BlogDetailView(request, slug):
    about = AboutAndQuote.objects.all()
    blogs = Blog.objects.get(slug=slug)
    related_blogs = Blog.objects.filter().exclude(slug=slug) 
    return render(request, 'website/blog/blogdetail.html', {'blog' : blogs, 'related_blogs' : related_blogs,'about' : about})


def BlogPostView(request):
    return render(request,'website/blog/blogs.html',  context)

    

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



