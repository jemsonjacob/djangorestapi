from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):
    book_name=models.CharField(max_length=100)
    author=models.CharField(max_length=50)
    price=models.PositiveIntegerField(null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.book_name
