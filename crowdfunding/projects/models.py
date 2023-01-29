from django.db import models

from django.db.models import Sum, Avg, Count, Min

from django.contrib.auth import get_user_model

User = get_user_model()
# this is telling django to get the users model from the settings. This is just defining an alias.

#in the class Project model, because we haven't said anything has to be true, the default is automatically true.
#auto_now_add = means that when you create a project, it will always add the current date and time.
#HINT from Ben 14/1/23 = owner needs to be changed to foreign key field.

# “A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.”


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name='owner_projects')

    @property
    def total(self):
        return self.pledges.aggregate(sum=models.Sum('amount'))['sum']

    category = models.ForeignKey(
        'Category',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='project_id')
    
  # liked_by = models.ManyToManyField(
    #     User, 
    #     related_name='liked_projects'
    # )
    
    # liked_by = models.ManyToManyField(
    #     User, related_name='liked_projects')


# Used to Create Project Categories
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
  
# properties are a way of returning a value as if it was a database field

# related_name is how the relationship works backwards. SO from Project the owner is project.owner (which is a user), so project1.owner will be a user. this is a foreign key to the user. from customer user back is the related name, so customuser.projects is relating back.
class Pledge(models.Model):
    amount = models.IntegerField(default=1)
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, 
        related_name="pledges")
    supporter = models.ForeignKey(User, on_delete=models.CASCADE, 
    related_name='supporter_pledges')

# on_delete models.CASCADE deletes everything related to that individual pledge, OR individual project.

