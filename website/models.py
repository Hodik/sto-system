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
    location = models.CharField(max_length=300)
    discription = models.TextField()
    website = models.TextField()

    def get_average_rating(self):
        rv: int = 0.0
        counter: int = 0.0
        for review in self.sto_reviews.all():
            rv += review.rating
            counter += 1
        try:
            return rv / counter
        except:
            return None

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_reviews")
    sto = models.ForeignKey(Sto, on_delete=models.CASCADE, related_name="sto_reviews")
    text = models.TextField()
    rating = models.IntegerField()



