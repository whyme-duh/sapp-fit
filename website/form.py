from django import forms
from django.utils import timezone
from website.models import Booking, Client, Service


class BookingForm(forms.Form):

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})) 
    phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}))          
    preferred_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': timezone.localdate().isoformat(),
                'class': 'form-control'
            }
        )
    )
    service_type = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 
                                                                                 'value': '',
                                                                                 'disabled': 'disabled'}))
        

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = "__all__"  



  
