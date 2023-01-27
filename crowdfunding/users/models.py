from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    def __str__(self):
        return self.username
        
# __str__ is a dunder method , when you do this, it returns this.
# CLass is creating constraints definition, capability

