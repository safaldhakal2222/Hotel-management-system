from django.db import models

# Create your models here.



class Room(models.Model):
    ROOM_TYPES = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    )

    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.FloatField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"{self.customer} - {self.room}"