from django.urls import path
from . import views

urlpatterns = [
    path('', views.ideas_list, name='ideas_list'),
]
