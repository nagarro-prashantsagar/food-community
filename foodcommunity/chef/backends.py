from django.contrib.auth.backends import ModelBackend
from .models import Chef

class ChefAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            chef = Chef.objects.get(email=username)
            if chef.check_password(password):
                return chef
        except Chef.DoesNotExist:
            return None
