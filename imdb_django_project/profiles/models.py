from django.db import models

class Actor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    bio = models.TextField(null=True)
    birth_date = models.DateField(null=True)