from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserCreateView, UserDetailView, UserDashboardAPIView

urlpatterns = [
    # JWT Login/Auth
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User CRUD & Custom Endpoints
    path('register/', UserCreateView.as_view(), name='register'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('dashboard/', UserDashboardAPIView.as_view(), name='dashboard'),
]