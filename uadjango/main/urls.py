from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Index.as_view(), name='main'),
]