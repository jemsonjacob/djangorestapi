from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    task_name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.task_name
