from django.urls import path
from .views import CourseListCreateView, CourseDetailView, CourseEnrollAPIView

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', CourseEnrollAPIView.as_view(), name='course_enroll'),
]