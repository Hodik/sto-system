from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BaseModel(models.Model):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Sto(BaseModel):
    name = models.CharField(unique=True, max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stos")

