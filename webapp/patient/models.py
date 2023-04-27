from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class Patient(AbstractUser, PermissionsMixin):
    GENDER_CHOICES = [
        ("M", "Male"), 
        ("F", "Female"),
        ("O", "Other")
    ]
    
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()
    health_condition_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} health profile"
