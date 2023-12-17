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
    



class UserLoginView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        



class UserSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserSearchPagination

    def get_queryset(self):
        queryset = UserProfile.objects.all()

        # Retrieve search parameter from query parameter
        search_query = self.request.query_params.get('search', None)

        if search_query:
            # Check if the search query is a valid email
            try:
                user_profile = UserProfile.objects.get(user__email__iexact=search_query)
                return UserProfile.objects.filter(id=user_profile.id)
            except UserProfile.DoesNotExist:
                pass

            # If the search query is not a valid email, search by name containing the substring
            queryset = queryset.filter(name__icontains=search_query)

        return queryset
