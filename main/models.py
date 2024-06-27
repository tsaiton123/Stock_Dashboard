# Create your models here.
from django.db import models


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker
