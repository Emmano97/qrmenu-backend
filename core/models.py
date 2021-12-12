from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimestampModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Place(TimestampModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    number_of_tables = models.IntegerField(default=1)
    font = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.owner.username} / {self.name}"


class Category(TimestampModel):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.place} / {self.name}"

class MenuItem(TimestampModel):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    image = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.category} / {self.name}"

class  Order(TimestampModel):
    PROCESSING_STATUS = 'processing'
    COMPLETED_STATUS = "completed"
    STATUSES = (
        (PROCESSING_STATUS, 'Processing'),
        (COMPLETED_STATUS, 'Completed'),
    )

    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    table = models.CharField(max_length=2)
    detail = models.TextField()
    payment_intent = models.CharField(max_length=255)
    amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUSES, default=
    PROCESSING_STATUS)

    def __str__(self):
        return f"{self.place}/{self.table}/${self.amount}"


