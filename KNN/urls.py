from django.urls import path
from . import views

urlpatterns = [
    path('knn/', views.knn_model, name='home'),
    path('predict/', views.predict, name='predict'),
    path('api/predict/', views.api_predict, name='api_predict'),
]

