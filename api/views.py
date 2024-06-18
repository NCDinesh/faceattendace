from django.shortcuts import render
from rest_framework import viewsets
from api.serializer import CourseSerializer
from api.models import Course

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Create your views here.
