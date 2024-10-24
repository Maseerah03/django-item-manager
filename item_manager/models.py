from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_description = models.TextField()
    item_code = models.CharField(max_length=100)
    item_qty = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_name = models.CharField(max_length=255)

    def __str__(self):
        return self.item_name
