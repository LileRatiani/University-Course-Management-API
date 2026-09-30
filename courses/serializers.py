from rest_framework import serializers
from .models import Course, Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # This will nest the assignment data inside the course JSON
    assignments = AssignmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'professor', 'students', 'max_capacity', 'created_at', 'assignments']
        read_only_fields = ['professor', 'students']