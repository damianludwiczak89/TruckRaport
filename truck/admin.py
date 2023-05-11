from django.contrib import admin
from .models import User, Truck, Tour, Spedition

# Register your models here.
admin.site.register(User)
admin.site.register(Truck)
admin.site.register(Tour)
admin.site.register(Spedition)

