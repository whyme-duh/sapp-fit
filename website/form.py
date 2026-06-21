from django import forms
from django.utils import timezone
from website.models import Booking, Client, CustomService, Service


class BookingForm(forms.Form):

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})) 
    phone_number = forms.IntegerField( widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength' : 10}))          
    preferred_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': timezone.localdate().isoformat(),
                'class': 'form-control'
            }
        )
    )
    service_type = forms.ModelChoiceField(
        required=True,
        queryset=Service.objects.all(),
        empty_label="Select a service",
        widget=forms.Select(
            attrs={'class': 'form-control', 
            }))
    

    def clean(self):
        super(BookingForm, self).clean()
        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number)) != 10:
            self._errors['phone_number'] = self.error_class(['Please enter valid phone number with 10 digits.'])
        return self.cleaned_data
    

class OneServiceBookingForm(forms.Form):

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})) 
    phone_number = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength' : 10}))          
    preferred_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': timezone.localdate().isoformat(),
                'class': 'form-control'
            }
        )
    )
    service_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 
                   'disabled': 'disabled'
            }))
    

    def clean(self):
        super(OneServiceBookingForm, self).clean()
        valid_prefixes = (
            '984', '985', '986', '974', '975', '980', '981', 
            '982', '970', '971', '961', '962', '988'
        )
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number:

            phone_number_str= str(phone_number)

            if len(str(phone_number)) != 10:
                self._errors['phone_number'] = self.error_class(['Please enter valid phone number with 10 digits.'])

            elif not phone_number_str.startswith(valid_prefixes):
                self.add_error('phone_number', 'The provided number does not start with a valid Nepali carrier prefix.')
        return self.cleaned_data

        

class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = "__all__"  

    def clean(self):
        super(ClientForm, self).clean()
        age = self.cleaned_data['age']

        if age <10 or age > 100:
            self._errors['age'] = self.error_class(["Please enter valid age!"]) 
        return self.cleaned_data


class CustomServiceForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'})) 
    phone_number = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}))          
    goal_choices = forms.ChoiceField(
        choices=CustomService.GOAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    special_notes = forms.CharField(
        max_length=500,
        required = False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Any special notes or requirements', 'rows': 3}
        )
    )
    equipment_used = forms.CharField(
        max_length=500,
        required = False,
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Equipment you plan to use', 'rows': 3}
        )
    )
    preferred_duration = forms.ChoiceField(
        choices=CustomService.PLAN_DURATION_OPTIONS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    workout_time = forms.ChoiceField(
        choices=CustomService.WORKOUT_TIME_OPTIONS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    age = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Age'}))
    weight = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your Weight in kg'}))
    gender  = forms.ChoiceField(
        choices=CustomService.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    activity_level = forms.ChoiceField(
        choices=CustomService.ACTIVITY_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )   

    def clean(self):
        super(CustomServiceForm, self).clean()
        age = self.cleaned_data['age']
        weight = self.cleaned_data['weight']
        phone = self.cleaned_data['phone_number']
        if age < 10 or age > 60:
            self._errors['age'] = self.error_class(['I can only provide services to people aged 10 to 60.'])
        if weight < 40 or weight > 100:
            self._errors['weight'] = self.error_class(['Please enter a valid weight in kg.'])
        if len(phone) != 10:
            self._errors['phone_number'] = self.error_class(['Please enter valid phone number with 10 digits.'])
        return self.cleaned_data