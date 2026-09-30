from django.urls import path
from .views import (
    CourseListCreateView, CourseDetailView, CourseEnrollAPIView,
    AssignmentListCreateView, AssignmentDetailView,
    SubmissionListCreateView, GradeSubmissionView
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course_list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/enroll/', CourseEnrollAPIView.as_view(), name='course_enroll'),

    path('assignments/', AssignmentListCreateView.as_view(), name='assignment_list'),
    path('assignments/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),

    # New Submission Endpoints
    path('submissions/', SubmissionListCreateView.as_view(), name='submission_list'),
    path('submissions/<int:pk>/grade/', GradeSubmissionView.as_view(), name='submission_grade'),
]