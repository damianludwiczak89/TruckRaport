from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    default_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1.3)
    
    def __str__(self):
        return f"{self.username}"

    def serialize(self):
        return {
            "id": self.id,
            "default_rate": self.default_rate,
        }
    
class Truck(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="Default")

    def __str__(self):
        return f"{self.name}"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Spedition (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }
    
class Tour(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    freight = models.DecimalField(max_digits=10, decimal_places=2)
    km = models.IntegerField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    date= models.DateField()
    spedition = models.ForeignKey(Spedition, on_delete=models.CASCADE, related_name="sped")

    def __str__(self):
        return f"(Tour for {self.truck} on {self.date})"
    
    def serialize(self):
        return {
            "id": self.id,
            "freight": self.freight,
            "km": self.km,
            "rate": self.rate,
            "date": self.date,
            "spedition": self.spedition.id,
        }
    
