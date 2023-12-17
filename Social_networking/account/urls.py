from django.urls import path
from .views import UserProfileAPIView, UserAPIView,UserSearchView

urlpatterns = [
    path('user/', UserAPIView.as_view(), name='userapi'),
    path('userprofiles/', UserProfileAPIView.as_view(), name='userprofile'),
    path('usersearch/', UserSearchView.as_view(), name='usersearch'),


]
