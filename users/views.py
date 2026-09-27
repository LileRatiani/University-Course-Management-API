from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsSelfOrAdmin

# 1. Generic View: Create (Register)
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# 2. Generic View: Read, Update, Delete (CRUD)
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]

# 3. Custom APIView
class UserDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Welcome to the University Portal, {request.user.username}!",
            "role": request.user.role,
            "department": request.user.department
        })