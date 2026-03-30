from django.contrib import admin
from .models import User
from .models import Location, Cart, CartLocationHistory

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Cart)
admin.site.register(CartLocationHistory)


