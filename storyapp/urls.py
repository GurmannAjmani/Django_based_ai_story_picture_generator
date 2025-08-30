from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_form, name='story_form'),
]
