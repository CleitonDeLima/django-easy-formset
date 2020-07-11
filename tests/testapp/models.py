from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=10)
    bio = models.TextField()
