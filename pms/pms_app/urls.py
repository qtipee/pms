from django.urls import path
from .views import *

urlpatterns = [
    path('', Upload.as_view()),
    path('api/upload', Upload.as_view()),
    path('api/images', Images.as_view()),
    path('api/image/<int:id>', Image.as_view()),
]
