from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=300,)
    release = models.IntegerField(blank=False)

    def __str__(self):
        return self.title