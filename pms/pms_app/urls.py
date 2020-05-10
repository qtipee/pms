from django.urls import path
from .views import *

urlpatterns = [
    path('', Upload.as_view()),
    path('api/upload', Upload.as_view()),
    path('api/process/<str:filename>', Process.as_view()),
    path('api/images', Images.as_view()),
    path('api/image/<int:id>', Image.as_view()),
    path('api/image_file/<int:image_id>/<str:image>', ImageFile.as_view()),
    path('api/update/<int:image_id>/<int:count>', ImageCountUpdate.as_view()),
]
