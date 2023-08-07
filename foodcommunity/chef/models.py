from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model


class Chef(AbstractUser):
    # username = models.CharField(max_length=20)
    cuisine_specialty = models.ForeignKey('Cuisine', on_delete=models.SET_NULL, null=True)
    restaurant_name = models.CharField(max_length=100)
    experience_years = models.IntegerField(validators=[MinValueValidator(0)], null=True, default=0)
    short_info = models.TextField(max_length=300, null=True)
    is_online = models.BooleanField(default=False)
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True,

                                              related_name='chef_user_permissions')
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Chef'
        verbose_name_plural = 'Chefs'


# User = get_user_model()


class Cuisine(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class Chat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     chef = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Chat between {self.user} and {self.chef}"
#
#
# class ChatMessage(models.Model):
#     chat = models.ForeignKey('Chat', related_name='messages', on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Message in {self.chat} from {self.sender}"
