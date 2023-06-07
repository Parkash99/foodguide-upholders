from django.db import models
from django.db.models import Avg

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu_images/')
    description = models.TextField()
    category = models.CharField(max_length=50, default='Other')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def get_rating_stars(self):
        # Calculate the average rating for the MenuItem
        avg_rating = Order.objects.filter(item_name=self.title).aggregate(Avg('star_rating'))['star_rating__avg']
        
        if avg_rating is not None:
            return range(round(avg_rating))  # Return a range representing the average rating as stars
        return []  # Return an empty list if no ratings exist

class Order(models.Model):
    order_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    star_rating = models.IntegerField(default=5)

    def __str__(self):
        return self.order_id
