from django.contrib import admin
from .models import UserProfile, JobListing

# Register your models here.


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'location', 'created_at')  # Show these fields in the list
    search_fields = ('title', 'company', 'location')  # Enable search
    list_filter = ('location', 'created_at')  # Add filtering options
    ordering = ('-created_at',)  # Sort by newest jobs first

admin.site.register(UserProfile)
