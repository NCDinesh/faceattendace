
from django.urls import path,include
from .views import CourseViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'courses',CourseViewSet)

urlpatterns = [
    path('',include(router.urls))
]
