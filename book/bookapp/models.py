from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class locations(models.Model):
    location_name=models.TextField(max_length=200,)

class Category(models.Model):
    name=models.TextField(max_length=200,unique=True)

class genres(models.Model):
    cat_name=models.ForeignKey(Category,on_delete=models.CASCADE)
    ge_name=models.TextField(max_length=200)

class books(models.Model):
    title = models.CharField(max_length=200)
    auther = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    location = models.ForeignKey('locations', on_delete=models.CASCADE, null=True, blank=True)
    genre = models.ForeignKey('genres', on_delete=models.CASCADE)
    cover_image = models.FileField()
    available_copies = models.IntegerField(default=2)

class Borrow(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Returned', 'Returned'),
        ('Return Requested', 'Return Requested'),
    ]
    book = models.ForeignKey(books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    approval_date = models.DateField(null=True, blank=True) 
    r_date = models.DateField(null=True, blank=True)  # Only set when approved
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    return_request_date = models.DateField(null=True, blank=True)  # Date when user requests to return
    return_approval_date = models.DateField(null=True, blank=True)  # Date when admin approves return
 


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

 


