from django.urls import path

from users.views import UserLogInView
from users.views import UserRegisterApiView
from users.views import UserListAPIView
from users.views import UserFiendListAPIView
from users.views import UserPendingListAPIView
from users.views import SendRequestAPIView
from users.views import AcceptRequestAPIView
from users.views import DeleteRequestAPIView


urlpatterns = [
    # (POST request)
    path('register/', UserRegisterApiView.as_view(), name='register_api'),
    
    # (POST request)
    path('login/', UserLogInView.as_view(), name='login_api'),
    
    # (Get request) api to list all users 
    path('users/', UserListAPIView.as_view(), name='user_list_api'),
    
     # (Get request) api to list actual fiends 
    path('friend/list/', UserFiendListAPIView.as_view(), name='friend_list_api'),

    # (Get request) api to list pending friend request 
    path('pending/list/', UserPendingListAPIView.as_view(), name='pending_list_api'),
    
    # (Post request) route for sending friend requests 
    path('send/request/<int:receiver_id>/', SendRequestAPIView.as_view(), name='send_request_api'),
    
    #  (PUT request)
    path('accept/<int:friend_id>/', AcceptRequestAPIView.as_view(), name='accept_request_api'),
    
    # (Delete request)
    path('delete/<int:friend_id>/', DeleteRequestAPIView.as_view(), name='delete_request_api'),
]
