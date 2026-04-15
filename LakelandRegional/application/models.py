from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

#| Field          | Type            | Description                 |
#| -------------- | --------------- | --------------------------- |
#| `username`     | `CharField`     | Unique identifier for login |
#| `first_name`   | `CharField`     | User's first name           |
#| `last_name`    | `CharField`     | User's last name            |
#| `email`        | `EmailField`    | User’s email                |
#| `password`     | `CharField`     | Hashed password             |
#| `is_staff`     | `BooleanField`  | Can log into admin site     |
#| `is_active`    | `BooleanField`  | Active account status       |
#| `is_superuser` | `BooleanField`  | Superuser privileges        |
#| `last_login`   | `DateTimeField` | Last login timestamp        |
#| `date_joined`  | `DateTimeField` | Account creation timestamp  |




class Location(models.Model):

    LOCATION_CHOICES = [
        ('hallway1',    "Hallway 1"),
        ("hallway2",    "Hallway 2"),
        ("hallway3",    "Hallway 3"),
        ("washroom",    "Wash Room"),
        ("washhall",    "Wash Hall"),
        ("cleanroom",   "Clean Room"),
        ("storageroom", "Storage Room"),
    ]
    name = models.CharField(max_length=100, choices=LOCATION_CHOICES) # e.g., "SPD", "OR", "ICU"
    rfid_reader_id = models.CharField(max_length=100, unique=True) # unique identifier for the RFID reader at this location

    def __str__(self):  #this
        return self.name
    


class Cart(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'), # this means that it is being washed or repaired
    ]

    name = models.CharField(max_length=100) # e.g., "Cart 1", "Cart 2"
    rfid_tag = models.CharField(max_length=100, unique=True) # this is the unique identifier for the cart's RFID tag
    current_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True) # current location of the cart, can be null if not tracked

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available') # current status of the cart
    last_seen = models.DateTimeField(null=True, blank=True) # DateTimeFiled function to allow for specific times to be seeded

    #last_seen = models.DateTimeField(auto_now=True) # timestamp of the last time the cart was seen by an RFID reader

    def __str__(self):
        return self.name



class CartLocationHistory(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # the cart being tracked
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True) # the location where the cart was seen
    timestamp = models.DateTimeField(auto_now_add=True) # when the cart was seen at this location

    class Meta:
        ordering = ['-timestamp'] # order by most recent first

    def __str__(self):
        return f"{self.cart.name} at {self.location.name} on {self.timestamp}"