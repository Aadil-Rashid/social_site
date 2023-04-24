from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from users.managers import UserManager
from users.managers import FriendshipManager

from users.constants import FRENDSHIP_STATUS


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    @property
    def active_user(self):
        return self.is_active


class OutstandingToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='outstanding_token')
    jti = models.CharField(unique=True, max_length=255)
    token = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )
        

class Friendship(models.Model):
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                    related_name='friendship_requests_received')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, 
                    related_name='friendship_requests_sent')
    status = models.CharField(choices=FRENDSHIP_STATUS, default='pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = FriendshipManager()

    def __str__(self):
        return f'{self.sender.name} -> {self.receiver.name} ({self.status});'

