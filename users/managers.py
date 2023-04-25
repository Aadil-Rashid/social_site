from django.db.models import Q
from django.utils import timezone
from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager

from datetime import timedelta

from users.constants import PENDING
from users.constants import ACCEPTED
from users.constants import REJECTED

from rest_framework import status


class UserManager(BaseUserManager):
    def create_user(self, email, password, name=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        if name:
            user.name = name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user 
    
    def search(self, search):
        return self.filter(Q(email__icontains=search)|Q(name__icontains=search))
 
class FriendshipManager(Manager):
    def get_friends(self, user):        
        return self.filter(receiver=user, status=ACCEPTED) 
        
    def get_pending_requests(self, user):        
        return self.filter(receiver=user, status=PENDING)

    def create_request(self, user_id, receiver_id):
        if user_id == receiver_id:
            message = "Cannot send a friend request to oneself"
            status_code = status.HTTP_400_BAD_REQUEST
            return message, status_code
    
        obj = self.filter(sender_id=user_id, receiver_id=receiver_id).exclude(Q(status=REJECTED))
        if obj:
            message = {f'Friendship Instance Already Present {obj}'}    
            status_code = status.HTTP_201_CREATED
        else:
            now = timezone.now()
            one_minute_ago = now - timedelta(minutes=1)
            count = self.filter(sender_id=user_id, created_at__gte=one_minute_ago).count()
            if count >= 3:
                message = "Cannot send more than 3 friend requests within a minute"
                status_code = status.HTTP_400_BAD_REQUEST
                return message, status_code
            created_obj = self.create(sender_id=user_id, receiver_id=receiver_id)
            status_code = status.HTTP_201_CREATED
            message = f"Friendship Instance Created, {created_obj}" 
        return message, status_code
    
    def accept_request(self, sender_id, receiver_id):
        message = ''
        obj = self.filter(sender_id=sender_id, receiver_id=receiver_id).exclude(Q(status=REJECTED)).first()
        if not obj:
            return None, {'Friendship instance not found'}
        if obj.status == ACCEPTED:
            message = 'Friend Request Already Accepted'
        else:
            obj.status = ACCEPTED
            obj.save()
        return obj, message
    
    def reject_request(self, sender_id, receiver_id):
        obj = self.filter(sender_id=sender_id, receiver_id=receiver_id).exclude(Q(status=REJECTED)).first()
        if not obj:
            return None
        obj.status = REJECTED
        obj.save()
        return obj
        
