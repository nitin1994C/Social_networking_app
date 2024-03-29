from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import UserProfile, Friendship, User
from account.serializers import UserProfileSerializer, UserSerializer
from .serializers import FriendshipSerializer
from rest_framework.authentication import TokenAuthentication
from django.db import models
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle


class SendFriendRequestView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer

    def perform_create(self, serializer):
        sender_id = self.request.data.get('sender')
        receiver_id = self.request.data.get('receiver')

        try:
            sender = User.objects.get(id=sender_id)
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            # If the sender or receiver doesn't exist, return an error response
            return Response({"detail": "Sender or receiver does not exist."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Create the Friendship object
        friendship = Friendship.objects.create(sender=sender, receiver=receiver, status='pending')

        # Serialize and return the response
        serializer = FriendshipSerializer(friendship)
        return Response(serializer.data, status=status.HTTP_201_CREATED)





class AcceptFriendRequestView(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()  

    def update(self, request, *args, **kwargs):
        friendship = self.get_object()
        print(f"Friendship Status: {friendship.status}")
        print(f"Receiver: {friendship.receiver}")
        print(f"Request User: {request.user}")
        print(self.request.user)

        if friendship.receiver == self.request.user and friendship.status == 'pending':
            friendship.status = 'accepted'
            friendship.save()
            return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)
        elif friendship.receiver == self.request.user and friendship.status == 'accepted':
            return Response({"detail": "You are already friends."}, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response({"detail": "No pending friend request from this user."}, status=status.HTTP_400_BAD_REQUEST)


class RejectFriendRequestView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FriendshipSerializer
    queryset = Friendship.objects.all()  # Specify the queryset

    def destroy(self, request, *args, **kwargs):
        friendship = self.get_object()

        if friendship.receiver == self.request.user and friendship.status == 'pending':
            friendship.delete()
            return Response({"detail": "Friend request rejected."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "No pending friend request from this user."}, status=status.HTTP_400_BAD_REQUEST)







class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = Friendship.objects.filter(
            (models.Q(sender=user) | models.Q(receiver=user)) &
            models.Q(status='accepted')
        )
        return friends

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        pending_requests = Friendship.objects.filter(receiver=user, status='pending')
        senders = [request.sender for request in pending_requests]
        return senders


