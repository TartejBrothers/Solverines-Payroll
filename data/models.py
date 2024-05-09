from django.db import models


# Create your models here.
class Database(models.Model):
    name = models.TextField()
    id = models.TextField(primary_key=True)

    salary = models.IntegerField()
    design = models.TextField()
    gender = models.TextField()
    pan_no = models.CharField(max_length=20)
    aadhar_no = models.BigIntegerField()
    dateofbirth = models.TextField()
    dateofjoining = models.TextField()
    bankname = models.CharField(max_length=100)
    ac_no = models.BigIntegerField()
    uan_no = models.CharField(max_length=20)
