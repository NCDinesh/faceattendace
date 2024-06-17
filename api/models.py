from django.db import models

class Course(models.Model):
    name=models.CharField( max_length=200)
    teachinghour = models.IntegerField()
    tutor = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Create your models here.
