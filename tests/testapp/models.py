from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=10)
    bio = models.TextField()


class Thing(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)


class Food(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)


class Home(models.Model):
    location = models.CharField(max_length=10)


class Person(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)


class Address(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
