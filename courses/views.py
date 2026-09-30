from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsProfessorOrReadOnly


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