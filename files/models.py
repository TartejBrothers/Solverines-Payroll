from django.db import models


# Create your models here.
class Values(models.Model):
    name = models.TextField()
    id = models.TextField(primary_key=True)
    dept = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    salary = models.IntegerField()
    designation = models.TextField()
    gender = models.TextField()
    pan_no = models.TextField()
    uan_no = models.IntegerField()
