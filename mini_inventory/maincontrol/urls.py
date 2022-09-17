from . import views
from django import urls
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('create_inventory/', views.create_inventory, name='create_inventory'),
    path('recieve_inventory/', views.recieve_inventory, name='recieve_inventory'),
    path('send_out_inventory/', views.send_out_inventory, name='send_out_inventory'),
    path('currently_managing_a/', views.currently_managing_a, name='currently_managing_a'),
    path('currently_managing_a/currently_managing_b/<int:pk>/', views.currently_managing_b, name='currently_managing_b'),
    path('view_all/', views.view_all, name='view_all'),
]