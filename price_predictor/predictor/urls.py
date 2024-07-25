# predictor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_price, name='predict_price'),
    path('analytics/', views.show_analytics, name='show_analytics'),
    path('get_analytics/', views.get_analytics, name='get_analytics'),
]
