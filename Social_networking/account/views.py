from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,UserProfileSerializer
from .models import User, UserProfile
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django.db import models
from django.db.models import Q


class UserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UserProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    




        



class UserSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        queryset = UserProfile.objects.all()

        # Retrieve search parameter from query parameter
        search_query = self.request.query_params.get('search', None)

        if search_query:
            # Check if the search query is a valid email
            queryset = UserProfile.objects.filter(
        models.Q(name__icontains=search_query) | models.Q(user__email__icontains=search_query))

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

