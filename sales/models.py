from django.db import models

# Create your models here.
from django.db import models
class Sale(models.Model):
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    item_type = models.CharField(max_length=20)
    sales_channel = models.CharField(max_length=10)
    order_priority = models.CharField(max_length=5)
    order_date = models.DateTimeField()
    order_id = models.IntegerField(primary_key=True)
    ship_date = models.DateField()
    units_sold = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = "sales"