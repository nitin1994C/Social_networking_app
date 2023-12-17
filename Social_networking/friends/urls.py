from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, ListFriendsView, ListPendingFriendRequestsView

urlpatterns = [
    path('send_friend_request/', SendFriendRequestView.as_view(), name='send_request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_request'),
    path('reject_friend_request/<int:pk>/', RejectFriendRequestView.as_view(), name='reject_request'),
    path('list_friends/', ListFriendsView.as_view(), name='list_friends'),
    path('pending_requests/', ListPendingFriendRequestsView.as_view(), name='pending_requests'),
]
