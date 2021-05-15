from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='products', default='no_picture.png')
    # logo will be stored inside media/
    price = models.FloatField(help_text='in US $')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str___(self):
        return f"{self.name} - {self.created_at.strftime('%d-%m-%Y')}"
