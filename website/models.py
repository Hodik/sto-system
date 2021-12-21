from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BaseModel(models.Model):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from abc import ABC, abstractmethod

class Sto(BaseModel):
    _STATE = None
    name = models.CharField(unique=True, max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stos")
    location = models.CharField(max_length=300)
    discription = models.TextField()
    website = models.TextField()
    status = models.CharField(max_length=300, null=False, default="inactive")

    def setState(self, state):
        self._STATE = state
        state._sto = self

    def presentStatus(self):
        print(f"Current status is {self._STATE.name}")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setState(get_STATE_by_name(self.status)())

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

def get_STATE_by_name(name: str):
    if name == "inactive":
        return inactive
    if name == "working":
        return working
    if name == "preparing":
        return preparing
    if name == "building":
        return building

class State(ABC):
    
    name = "state"
    allowed = []
    _sto = None

    @abstractmethod
    def search(self) -> bool:
        pass

    @abstractmethod
    def edit(self) -> bool:
        pass

    def toggle(self, state) -> bool:
        if state.name in self.allowed:
            return True
        return False
    
class inactive(State):
    name = "inactive"
    allowed = ["building"]

    def search(self) -> bool:
        return False

    def edit(self) -> bool:
        return True

class working(State):
    name = "working"
    allowed = []

    def search(self) -> bool:
        return True

    def edit(self) -> bool:
        return False

class building(State):
    name = "building"
    allowed = ["preparing", "working"]

    def search(self) -> bool:
        return False

    def edit(self) -> bool:
        return True

class preparing(State):
    name = "preparing"
    allowed = ["working"]

    def search(self) -> bool:
        return False

    def edit(self) -> bool:
        return False

class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_reviews")
    sto = models.ForeignKey(Sto, on_delete=models.CASCADE, related_name="sto_reviews")
    text = models.TextField()
    rating = models.IntegerField()



