from django import forms

from website.models import Client


class ContactForm(forms.Form):
    subject = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = "__all__"    
