# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
# class Cuisine(models.Model):
#     name = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.name
#
# class Chef(AbstractUser):
#     username = models.CharField(max_length=20)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     password = models.CharField(max_length=30)
#     email = models.EmailField()
#     cuisine_specialty = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True)
#     restaurant_name = models.CharField(max_length=100)
#     experience_years = models.PositiveIntegerField()
#
#     def __str__(self):
#         return self.username