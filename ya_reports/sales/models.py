from django.db import models

# Create your models here.
from django.utils import timezone
from django.shortcuts import reverse

from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from .utils import generate_code

class Position(models.Model):
    """
    A product name, quantity and price
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created_at = models.DateTimeField(blank=True) # auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # overwrite thesave method to set the price
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"id: {self.id} - {self.created_at.strftime('%d-%m-%Y')} - quantity: {self.quantity}"

class Sale(models.Model):
    """
    Can have many Positions
    """
    transaction_id = models.CharField(max_length=2, blank=True)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        if self.created_at is None:
            self.create_at = timezone.now()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sales:detail', kwargs={'pk': self.pk})
    
    def get_positions(self):
        return self.positions.all()

    def __str__(self):
        return f"Sales for the amount of $US {self.total_price}"

class CSV(models.Model):
    file_name = models.FileField(upload_to='cvs')
    activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name
