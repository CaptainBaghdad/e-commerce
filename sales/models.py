from django.conf import settings 
#from django.apps import AppConfig
from django.shortcuts import reverse

from django.db import models

CATEGORY_CHOICES = (
    ('S', 'shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('O', 'danger')
)

class Item(models.Model):

    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()
   

    def get_absolute_url(self):
        return reverse("products", kwargs={
            'slug': self.slug
        })
    
    def get_add_to_cart_url(self):
         return reverse("add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
         return reverse("remove-from-cart", kwargs={
            'slug': self.slug
        })


    
    
    def __str__(self):

        return self.title

   

    




class OrderedItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default= False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderedItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username