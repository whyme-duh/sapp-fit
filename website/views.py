import datetime
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
import threading

from idna import core
from sapfit import settings
from website.gemini_api import gemini_response
from .models import AboutAndQuote, Booking, Client, CoreValues, CustomService, Service, Blog, Testimonial
from django.contrib.auth.decorators import login_required
from  django.contrib import messages 
from django_ratelimit.decorators import ratelimit
from .form import BookingForm, ClientForm, CustomServiceForm, OneServiceBookingForm
from django.core.mail import send_mail
from django.db.models import Count

def page_not_found_404(request, exception):
    return render(request, 'website/error/404.html', status = 404)

def page_not_found_500(request):
    return render(request, 'website/error/500.html', status = 500)

def index(request):
    about = AboutAndQuote.objects.first()
    if about:
        tags_list = [tag.strip() for tag in about.tag.split(',')] if about.tag else []
    else:
        tags_list = []
    return render(request, 'website/home.html', {
        'about': about,
        'services': Service.objects.all(),
        'blogs': Blog.objects.all(),
        'date' :datetime.datetime.today().strftime("%Y"),
        'testimonials' : Testimonial.objects.all(),
        'debug': settings.DEBUG,
        "tags_list": tags_list
        }
    )

def about_me(request):
    about = AboutAndQuote.objects.first()
    core_values = CoreValues.objects.all()
    return render(request, 'website/about.html', {"about" : about, "core_values" : core_values})

def services(request):
    return render(request, 'website/service/servicelist.html', {"services": Service.objects.all()})


def send_email_about_booking(client_name, client_email,request_type, **kwargs):
    if request_type == "predefined-service":
        subject  = f"New Booking Request from {client_name}"
        message = f"""
        Great news! You have a new booking request.
        
        Client Name: {client_name}
        Client Email: {client_email}
        Requested Service: {kwargs.get('service_type', 'N/A')}
        Preferred Time: {kwargs.get('preferred_date', 'N/A')}
        
        Log into the SAPPFIT dashboard to approve or manage this booking.
        """
    elif request_type == "custom-service":
        subject  = f"New Custom Service Request from {client_name}"
        message = f"""
        You have received a new custom service request.
        
        Name: {client_name}
        Email: {client_email}
        Phone Number: {kwargs.get('phone_number', 'N/A')}
        Goal: {kwargs.get('goal_choices', 'N/A')}
        Special Notes: {kwargs.get('special_notes', 'N/A')}
        Equipment Used: {kwargs.get('equipment_used', 'N/A')}
        Preferred Duration: {kwargs.get('preferred_duration', 'N/A')}
        Workout Time: {kwargs.get('workout_time', 'N/A')}
        
        Log into the SAPPFIT dashboard to review this request.
        """
    else:
        subject = "New Booking/Service Request"
        message = f"You have received a new request from {client_name} ({client_email}). Please check the dashboard for details."
    try:
        send_mail(
            subject, 
            message, 
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_RECEIVER],
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
            return redirect('home-page')
        form = OneServiceBookingForm(request.POST)
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
                # email_thread = threading.Thread(target=send_email_about_booking, args=(name, email,"predefined-service"), kwargs={'service_type': service_type.title, 'preferred_date': preferred_date})
                # email_thread.start()
                messages.success(request, f'Your booking request has been sent! We will contact you soon.')
                return redirect('service-detail', slug = slug)
        else:
            messages.error(request, f'Error occured. Try again!')
            error_details = form.errors.as_text()
            print(error_details)
    else:
        form = OneServiceBookingForm()
    service = Service.objects.get(slug = slug)
    other_services = Service.objects.all().exclude(slug = slug)
    return render(request, 'website/service/servicedetail.html', context = {'service' : service, "other_services" : other_services, 'form':form})

@ratelimit(key='ip', rate='3/h', method= 'POST', block = False)
def custom_service_request(request):
    if request.method == "POST":
        was_limited = getattr(request, 'limited', False)
        if was_limited:
            messages.error(request, f'Too many booking requests from this IP. Please try again later.')
            return redirect('home-page')
        button_clicked = request.POST.get('action')
        form = CustomServiceForm(request.POST, action_type = button_clicked )
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            gender = form.cleaned_data['gender']
            goal_choices = form.cleaned_data['goal_choices']
            special_notes = form.cleaned_data['special_notes']
            equipment_used = form.cleaned_data['equipment_used']
            preferred_duration = form.cleaned_data['preferred_duration']
            workout_time = form.cleaned_data['workout_time']
            activity_level = form.cleaned_data['activity_level']
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            try:
                if button_clicked == "human_request":
                    phone_number = form.cleaned_data['phone_number']
                    email = form.cleaned_data['email']
                    if CustomService.objects.filter(
                            name=name, 
                            email=email, 
                            phone_number=phone_number, 
                            goal_choices=goal_choices, 
                            preferred_duration=preferred_duration,
                            workout_time=workout_time).exists():
                                messages.error(request, f'You have already submitted a similar custom service request.')
                    else:
                        CustomService.objects.create(
                            name=name,
                            email=email,
                            phone_number=phone_number,
                            goal_choices=goal_choices,
                            special_notes=special_notes,
                            equipment_used=equipment_used,
                            preferred_duration=preferred_duration,
                            workout_time=workout_time,
                            activity_level=activity_level,
                            age = age,
                            weight = weight,
                        )
                        email_thread = threading.Thread(target=send_email_about_booking, args=(name, email, "custom-service"), kwargs={
                            'phone_number': phone_number,
                            'goal_choices': goal_choices,
                            'special_notes': special_notes,
                            'equipment_used': equipment_used,
                            'preferred_duration': preferred_duration,
                            'workout_time': workout_time,
                            'activity_level': activity_level
                        })
                        # email_thread.start()
                        messages.success(request, f'Your custom service request has been submitted!')
                        return redirect('home-page')
                elif button_clicked == "ai_preview":
                    gemini_response_result = gemini_response(
                        duration=preferred_duration,
                        age=age,
                        gender=gender,
                        weight=weight,
                        goal=goal_choices,
                        equipment=equipment_used,
                        notes=special_notes,
                        workout_time=workout_time,
                        activity_level=activity_level
                    )
                    request.session['workout_plan'] = gemini_response_result
                    if is_ajax:
                        return JsonResponse({
                            "status" : "success",
                            "redirect_url" : redirect('ai-response'),
                            "error_redirect_url" : redirect('custom-service')
                        })
                    return redirect('ai-response')
            except Exception as e:
                print(f"Error processing custom service request: {e}")
                messages.error(request, f'Error occurred while submitting the request. Please try again.')
    else:
        form = CustomServiceForm()
    return render(request, 'website/service/customservicepage.html', {'form':form})

def ai_response(request):
    ai_workout_plan = request.session.get('workout_plan')
    if not ai_workout_plan:
        messages.error(request, f'No AI-generated workout plan found. Please submit a custom service request first.')
        return redirect('custom-service')
    try:
        import json
        workout_data = json.loads(ai_workout_plan)
    except json.JSONDecodeError:
        return redirect('custom-service')
    return render(request, 'website/service/geminiresponse.html', {'workout': workout_data})

def BlogDetailView(request, slug):
    blogs = Blog.objects.get(slug=slug)
    related_blogs = Blog.objects.filter().exclude(slug=slug) 
    return render(request, 'website/blog/blogdetail.html', {'blog' : blogs, 'related_blogs' : related_blogs})

def BlogPostView(request):
    return render(request,'website/blog/blogs.html',  {'blogs': Blog.objects.all()})

@login_required
def client_view(request):
    if not request.user.is_superuser:
        return redirect('home-page')
    active_clients_count = Client.objects.filter(status = "Ongoing").count()
    total_clients_count = Client.objects.all().count()
    clients = Client.objects.all().order_by("-status", "-started_training_from")
    # this is to find the most subscribed service name
    if clients:
        top_service = Service.objects.annotate(
                total_subs = Count('client')
            ).order_by('-total_subs').values_list('title', flat=True).first()
    else:
        top_service = None
    return render(request, 'website/clients/clients.html', {'clients' : clients,  "active_clients_count": active_clients_count, 'total_clients_count': total_clients_count, 'top_service' : top_service})

@login_required
def client_form(request):
    if not request.user.is_superuser:
        return redirect('home-page')
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            total_sessions = form.cleaned_data['total_sessions']
            gender = form.cleaned_data['gender']
            started_training_from = form.cleaned_data['started_training_from']
            services = form.cleaned_data['services']
            any_problem = form.cleaned_data['any_problem']
            status = form.cleaned_data['status']
            paid_or_not = form.cleaned_data['paid_or_not']
            if Client.objects.filter(
                    name = name, 
                    age = age, 
                    total_sessions = total_sessions, 
                    gender = gender, 
                    started_training_from = started_training_from, 
                    services = services,
                    status = status, 
                    paid_or_not = paid_or_not
                ).exists():
                    messages.error(request, "Error! It seems the entrie is already present.")
            else:
                Client.objects.create(
                    name = name, 
                    age = age, 
                    total_sessions = total_sessions, 
                    gender = gender, 
                    started_training_from = started_training_from, 
                    services = services,
                    any_problem = any_problem,
                    status = status, 
                    paid_or_not = paid_or_not
                )
                messages.success(request, f'New client succesfully added!')
            return redirect('client-view')
        else:
            messages.error(request, f'Error occured. Try again!')
    else:
        form = ClientForm()
    return render(request, 'website/clients/clientform.html', {'form' : form})

@login_required
def delete_client(request, id):
    if not request.user.is_superuser:
        return redirect('home-page')
    try:
        client = Client.objects.get(id = id)
        client.delete()
        messages.success(request, f'{client.name} was deleted successfully')
    except:
        messages.error(request, f'Failed to delete {client.name}')
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
            return redirect('client-view')
        else:
            messages.error(request, f"Failed to update the client's detail. Try again!")
    else:
        form = ClientForm(instance = client)
    return render(request, 'website/clients/clientform.html', {'form' : form, 'client' : client})