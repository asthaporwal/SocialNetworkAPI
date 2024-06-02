from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer
from rest_framework.authtoken.models import Token
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta


User = get_user_model()

class SignupView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        name = request.data.get('name')
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(email=email, password=password, name=name)
        print("Hi, I am a user {}".format(type(user)))
        if isinstance(user, User):  # Check if user is a User instance
            print("I am an istance of user yeyeye")
            token, created = Token.objects.get_or_create(user=user)
            print("HI proceeding further................... token created")
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "User creation failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class SearchUserView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if query:
            return User.objects.filter(Q(email__iexact=query) | Q(name__icontains=query))
        return User.objects.none()

class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        to_user_id = request.data.get('to_user')
        to_user = User.objects.get(id=to_user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status='pending').exists():
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=request.user, timestamp__gte=one_minute_ago).count()
        if recent_requests >= 3:
            return Response({"error": "Too many requests, please wait"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response({"message": "Friend request sent"})

class ManageFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, action):
        friend_request = FriendRequest.objects.get(id=id, to_user=request.user)
        if action == 'accept':
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({"message": "Friend request accepted"})
        elif action == 'reject':
            friend_request.status = 'rejected'
            friend_request.save()
            return Response({"message": "Friend request rejected"})
        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

class ListFriendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        friends = User.objects.filter(
            Q(sent_requests__to_user=request.user, sent_requests__status='accepted') |
            Q(received_requests__from_user=request.user, received_requests__status='accepted')
        ).distinct()
        return Response(UserSerializer(friends, many=True).data)

class ListPendingRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        return Response(FriendRequestSerializer(pending_requests, many=True).data)

