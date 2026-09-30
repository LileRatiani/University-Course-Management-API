from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, CourseEnrollAPIView,
    AssignmentListCreateView, AssignmentDetailView
)

urlpatterns = [
    # Course Endpoints
    path('', CourseListCreateView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', CourseEnrollAPIView.as_view(), name='course_enroll'),

    # Assignment Endpoints
    path('assignments/', AssignmentListCreateView.as_view(), name='assignment_list'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
]