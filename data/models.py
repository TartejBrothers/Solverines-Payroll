from django.db import models


# Create your models here.
class Database(models.Model):
    name = models.TextField()
    id = models.TextField(primary_key=True)
    dept = models.TextField()
    email = models.TextField()
    phone = models.TextField()
    salary = models.IntegerField()
    designation = models.TextField()
    gender = models.TextField()
    pan_no = models.TextField()
    aadhar_no = models.IntegerField()
    dateofbirth = models.TextField()
    dateofjoining = models.TextField()
    bankname = models.TextField()
    ac_no = models.IntegerField()
