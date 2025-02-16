from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=50)
    # Add any additional fields here
    pass
    
    
class Meta:
    swappable = "AUTH_USER_MODEL"


STATUS_CHOICES = [
    ('Open', 'Open'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Closed', 'Closed'),
]

class Bug(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    reporter = models.ForeignKey(User, related_name='reported_bugs', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assigned_bugs', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
