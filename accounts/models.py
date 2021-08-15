from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.base import Model
from warehouse.models import Warehouse
# Create your models here.

class UserType(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class User(AbstractUser):
        
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$', message="Phone number must be entered in the format: '+99999999")
    phone = models.CharField(validators=[phone_regex], max_length=13, blank=True)
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT, blank=True, null=True)
    image = models.ImageField(upload_to = 'static/files/user/', blank=True, null=True)    
    can_view_records = models.BooleanField(default=False)
    can_edit_records = models.BooleanField(default=False)
    warehouse = models.ManyToManyField(Warehouse, blank=True)
    def __str__(self):
        return self.username
