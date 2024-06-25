
from django.urls import path,include
from .views import CourseViewSet
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'courses',CourseViewSet)

urlpatterns = [
    path('api',include(router.urls)),
    path('', views.index, name='index'),
    path('video_feed', views.video_feed, name='video_feed'),
    path('stop_feed', views.stop_feed, name='stop_feed'),


]
