from django.db import models
import uuid


# Create your models here.
class Employee(models.Model):
    uuid = models.UUIDField(unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)


class Expense(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.CharField(max_length=128)
    created_at = models.DateTimeField()
    amount = models.FloatField()
    currency = models.CharField(max_length=5)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    expense_approved = models.BooleanField(default=False)