from django.db import models

# Create your models here
class Book(models.Model):
    rank = models.IntegerField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return self.author
