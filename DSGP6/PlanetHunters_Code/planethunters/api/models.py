from django.db import models

# Create your models here.
class Star(models.Model):
    star_id = models.CharField(max_length=20)
    author = models.TextField()

    def __str__(self):
        return self.star_id