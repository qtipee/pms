from django.urls import path
from .views import *

urlpatterns = [
    path('', Upload.as_view()),
    path('upload', Upload.as_view()),
]
