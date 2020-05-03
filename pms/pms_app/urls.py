from django.urls import path
from .views import *

urlpatterns = [
    path('', Upload.as_view()),
    path('upload', Upload.as_view()),
    path('images', Images.as_view()),
    path('image/<int:id>', Image.as_view()),
]
