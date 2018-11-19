""" Mapper URL Config """
from django.urls import path
from . import views

app_name = 'mapper'
urlpatterns = [
    path('', views.index, name='index'),
]