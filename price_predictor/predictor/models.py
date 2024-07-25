# predictor/models.py

from django.db import models

class Prediction(models.Model):
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Prediction for {self.date} at {self.price}"
