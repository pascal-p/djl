from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    likes = models.PositiveIntegerField(default=0)
    #
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class User(models.Model):
    ## we will just have id here + timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
