from rest_framework import serializers
from .models import Course, Assignment, Submission


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'assignment', 'student', 'content', 'grade', 'submitted_at']
        # Students cannot grade themselves, and the student ID will be auto-assigned
        read_only_fields = ['student', 'grade', 'submitted_at']

class GradeSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['grade']

class CourseSerializer(serializers.ModelSerializer):
    # This will nest the assignment data inside the course JSON
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'professor', 'students', 'max_capacity', 'created_at', 'assignments']
        read_only_fields = ['professor', 'students']