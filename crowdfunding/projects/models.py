from django.db import models

# Create your models here.

#in the class Project model, because we haven't said anything has to be true, the degault is automatically true.
#auto_now_add = means that when you create a project, it will always add the current date and time.
#HINT from Ben 14/1/23 = owner needs to be changed to foreign key field.

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=200)


class Pledge(models.Model):
    amount = models.IntegerField
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="pledges")
    supporter = models.CharField(max_length=200)
