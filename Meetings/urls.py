from django.urls import path
from . import views

urlpatterns = [
    path('vytvorit-schuzku/<int:pk>/', views.SchuzkaCreateView.as_view(), name='vytvorit_schuzku'),
]
