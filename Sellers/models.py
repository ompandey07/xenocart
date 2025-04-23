from django.db import models

# Create your models here.
class ProductModel(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home'),
        ('gaming', 'Gaming'),
        ('health', 'Health'),
        ('beauty', 'Beauty'),
        ('more', 'More'),
    ]

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    product_quantity = models.IntegerField()
    product_description = models.CharField(max_length=1000)
    product_image = models.ImageField(upload_to='Sellers/ProductImages/', null=True, blank=True)
    product_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='more')

    def __str__(self):
        return self.product_name