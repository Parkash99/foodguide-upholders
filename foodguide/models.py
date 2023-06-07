from django.db import models

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='menu_images/')
    description = models.TextField()
    category = models.CharField(max_length=50, default='Other')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def get_rating_stars(self):
        return range(self.rating)
