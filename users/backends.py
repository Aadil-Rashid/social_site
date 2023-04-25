from django.contrib.auth.backends import BaseBackend
from users.models import CustomUser   
        
        
class CustomRestJWTAuthentication(BaseBackend):
    
    def authenticate(self, request, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        if self.authenticate_user_details(email, password):
            return CustomUser.objects.filter(email=email).first()
        
    def authenticate_user_details(self, email, password):
        user_obj = CustomUser.objects.filter(email=email).first()
        if user_obj and user_obj.check_password(password):
            return True
        return False
    
    