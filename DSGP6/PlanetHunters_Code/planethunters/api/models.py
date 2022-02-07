from django.db import models

# Create your models here.
class Star(models.Model):
    star_id = models.CharField(max_length=20)
    author = models.TextField()

    def __str__(self):
        return self.star_id

class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_pass = models.CharField(max_length=20)
    user_stars = models.ManyToManyField(Star, verbose_name="list of stars")

    def __str__(self):
        return self.user_name