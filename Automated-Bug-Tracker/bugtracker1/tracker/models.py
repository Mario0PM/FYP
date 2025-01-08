from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Developer', 'Developer'),
        ('Tester', 'Tester'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Tester')

class Meta:
    swappable = "AUTH_USER_MODEL"

class Bug(models.Model):
    SEVERITY_CHOICES = [
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Open')
    reporter = models.ForeignKey(User, related_name='reported_bugs', on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, related_name='assigned_bugs', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
