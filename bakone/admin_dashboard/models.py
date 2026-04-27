from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class CompanyDocument(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'HR'),
        ('Finance', 'Finance'),
        ('IT', 'IT'),
        ('Legal', 'Legal'),
        ('Other', 'Other'),
    ]
    title = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    file = models.FileField(upload_to='company_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
