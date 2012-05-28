from django.db import models

# Create your models here.


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default='0')
    email = models.TextField(default='0')
    number = models.TextField(default='0')
    created = models.PositiveIntegerField(default=0)
    removed = models.PositiveIntegerField(null=True)
class Admin:
    pass
    list_display = ('id', 'name', 'email', 'number', 'created', 'removed')
def __str__(self):
    return self.id

class Port_info(models.Model):
    customer_id = models.PositiveIntegerField(default=0)
    ip = models.CharField(max_length=64)
    port = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    status = models.TextField(null=True)
    updated = models.PositiveIntegerField(null=True)
    removed = models.PositiveIntegerField(null=True)
    description = models.TextField(null=True)

class Admin:
    pass
    list_display = ('customer_id', 'ip', 'port', 'type', 'status', 'updated', 'removed', 'description')
def __str__(self):
    return self.customer_id

