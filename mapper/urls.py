""" Mapper URL Config """
from django.urls import path
from .views import MapperView

app_name = 'mapper'
urlpatterns = [
    path('', MapperView.as_view(), name='index'),
]
