from django import forms
from .models import JobListing

class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'company', 'location', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }