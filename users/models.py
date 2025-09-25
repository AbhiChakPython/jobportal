from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('RECRUITER', 'Recruiter'),
        ('JOB_SEEKER', 'Job Seeker'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='JOB_SEEKER')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return self.user.username if self.user else "No User"


class JobListing(models.Model):
    title = models.CharField(max_length=250, db_index=True)
    company = models.CharField(max_length=250)
    location = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['location']),
            models.Index(fields=['created_at']),
        ]
        permissions = [
            ("can_create_job", "Can create job"),
            ("can_apply_job", "Can apply for job"),
        ]

    def __str__(self):
        return self.title
