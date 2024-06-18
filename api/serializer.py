from rest_framework import serializers
from api.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','name','teachinghour', 'tutor')