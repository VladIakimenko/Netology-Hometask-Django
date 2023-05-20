from django.urls import path

from measurement.views import SensorViewSet, SensorDetailViewSet, ReadingViewSet


urlpatterns = [
    path('sensors/', SensorViewSet.as_view()),
    path('sensors/<pk>/', SensorDetailViewSet.as_view()),
    path('measurements/', ReadingViewSet.as_view()),
]
