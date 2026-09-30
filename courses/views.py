from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsProfessorOrReadOnly
from .models import Assignment
from .serializers import AssignmentSerializer
from rest_framework.exceptions import ValidationError
from .models import Submission
from .serializers import SubmissionSerializer, GradeSubmissionSerializer

# Generic View: List all assignments or create a new one
class AssignmentListCreateView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    # Reusing the permission so only professors can create assignments
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrReadOnly]

# Generic View: Retrieve, Update, or Delete a specific assignment
class AssignmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrReadOnly]


# Generic View: List and Create Courses
class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrReadOnly]

    def perform_create(self, serializer):
        # Automatically assign the logged-in professor to the course
        serializer.save(professor=self.request.user)


# Generic View: Retrieve, Update, Delete specific course
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfessorOrReadOnly]


# Custom APIView: Student Enrollment Logic
class CourseEnrollAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        if request.user.role != 'student':
            return Response({"detail": "Only students can enroll in courses."}, status=status.HTTP_403_FORBIDDEN)

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        # Rule 1: Cannot enroll in the same course twice
        if request.user in course.students.all():
            return Response({"detail": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

        # Rule 2: Course has a maximum capacity
        if course.students.count() >= course.max_capacity:
            return Response({"detail": "Course is at maximum capacity."}, status=status.HTTP_400_BAD_REQUEST)

        # If both checks pass, enroll the student
        course.students.add(request.user)
        return Response({"detail": f"Successfully enrolled in {course.title}!"}, status=status.HTTP_200_OK)


# Generic View: Students list their submissions and create new ones
class SubmissionListCreateView(generics.ListCreateAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Students only see their own submissions
        if user.role == 'student':
            return Submission.objects.filter(student=user)
        # Professors see all submissions for courses they teach
        elif user.role == 'professor':
            return Submission.objects.filter(assignment__course__professor=user)
        return Submission.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'student':
            raise ValidationError("Only students can submit assignments.")

        assignment = serializer.validated_data['assignment']
        if user not in assignment.course.students.all():
            raise ValidationError("You cannot submit to a course you are not enrolled in.")

        serializer.save(student=user)


# Generic View: Professors grade a specific submission
class GradeSubmissionView(generics.UpdateAPIView):
    queryset = Submission.objects.all()
    serializer_class = GradeSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        submission = self.get_object()
        # Only the professor who teaches the course can grade it
        if self.request.user != submission.assignment.course.professor:
            raise ValidationError("Only the professor of this course can grade this submission.")

        serializer.save()