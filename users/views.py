from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializer import UserListSerializer
from users.serializer import FriendshipSerializer
from users.serializer import RegisterSerializer

from users.models import CustomUser
from users.models import Friendship

from users.pagination import CustomPagination

    
class UserLogInView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'please pass email & password in reqeust data'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)


class UserRegisterApiView(GenericAPIView):
    permission_classes = []
    serializer_class = RegisterSerializer
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            "user": UserListSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token at http://127.0.0.1:8000/api/login/",
        })


class UserListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self, search):
        if search:
            query_set = CustomUser.objects.search(search)
        else:
            query_set = CustomUser.objects.all()
        return query_set
    
    def list(self, request):
        search = request.query_params.get('search', '').strip()
        query_set = self.get_queryset(search)
        page = self.paginate_queryset(query_set)
        if page:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data)
      

class UserFiendListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer
    
    def get_queryset(self, user):
        query_set = Friendship.objects.get_friends(user)
        return query_set
            
    def list(self, request, *args, **kwargs):
        user = request.user       
        query_set = self.get_queryset(user)
        count = query_set.count()
        info = f"{user.name.title()} has total of {count} Friends :) "
        serializer = self.get_serializer(query_set, many=True)
        data = {info: serializer.data}
        return Response(data)


class UserPendingListAPIView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer
    
    def get_queryset(self, user):
        query_set = Friendship.objects.get_pending_requests(user.id)
        return query_set

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user:
            return Response({'error': 'user with id {user_id} not found'})
            
        query_set = self.get_queryset(user)
        count = query_set.count()
        name = user.name.title()
        info = f"{name} has total of = {count} Pending Friend Requests (: "
        serializer = self.get_serializer(query_set, many=True)
        data = {info: serializer.data}
        return Response(data)


class SendRequestAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        receiver_id = self.kwargs.get('receiver_id')
        if user_id == receiver_id:
            message = "Sender id can't be equal to Receiver id"
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            message, status_code = Friendship.objects.create_request(user_id, receiver_id)     
        return Response(message, status=status_code)


class AcceptRequestAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    #  accept request
    def put(self, request, *args, **kwargs):
        receiver_id = request.user.id
        sender_id = self.kwargs.get('friend_id')
        obj, message = Friendship.objects.accept_request(sender_id, receiver_id)
        status_code = status.HTTP_202_ACCEPTED
        if message:
            message = message
        elif  obj:
            message = {f'success: Friend Request Accepted, {obj}'}
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            message = {'Friendship instance not found'}
            
        return Response(message, status=status_code)
    
    
class DeleteRequestAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    # delete request
    def delete(self, request, *args, **kwargs):
        receiver_id = request.user.id
        sender_id = self.kwargs.get('friend_id')
        obj = Friendship.objects.reject_request(sender_id, receiver_id)
        if  obj:
            status_code = status.HTTP_202_ACCEPTED
            message = {f'Friend Requested Deleted: {obj}'}
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            message = {'Friendship instance not found'}
            
        return Response(message, status=status_code)
    
    