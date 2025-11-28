from django.contrib.auth.models import User
from django.db import models

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=200)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id
