from django.db import models

from django.db.models import Model

class StudentModel(Model):

    rno=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    mobile=models.CharField(max_length=50)
    year=models.CharField(max_length=50)
    section=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)
    photo = models.FileField(upload_to="images")

class PassRequestModel(Model):

    date=models.CharField(max_length=50)
    time=models.CharField(max_length=50)
    reason=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    studentid=models.CharField(max_length=50)