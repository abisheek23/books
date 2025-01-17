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

class Borrow(models.Model) :
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(books,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    r_date=models.DateField()


     


