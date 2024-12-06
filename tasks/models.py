
                             
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):  # Removed duplicate `models` in class declaration
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links task to a user
    title = models.CharField(max_length=255)  # Title of the task
    description = models.TextField(blank=True)  # Optional description
    category = models.CharField(max_length=50, default='General')  # Task category
    priority = models.CharField(  # Priority of the task with choices
        max_length=20,
        choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')],
        default='Medium'
    )
    deadline = models.DateTimeField(null=True, blank=True)  # Optional deadline
    completed = models.BooleanField(default=False)  # Task completion status
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-generated timestamp

    def __str__(self):  # Corrected function name and indentation
        return f"{self.title} (by {self.user.username})"
