from . import views
from django import urls
from django.urls import path

urlpatterns = [
    path('', views.eoq, name='eoq'),
    path('min_level/', views.minimum_level, name='min_level'),
    path('max_level/', views.maximum_level, name='max_level'),
    path('rol/', views.reorder_level, name='rol'),
]