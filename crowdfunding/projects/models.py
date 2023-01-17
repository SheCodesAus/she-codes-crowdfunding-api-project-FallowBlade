from django.db import models

# Create your models here.

#in the class Project model, because we haven't said anything has to be true, the default is automatically true.
#auto_now_add = means that when you create a project, it will always add the current date and time.
#HINT from Ben 14/1/23 = owner needs to be changed to foreign key field.

# “A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.”

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=200)


class Pledge(models.Model):
    amount = models.IntegerField(default=1)
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="pledges")
    supporter = models.CharField(max_length=200)
