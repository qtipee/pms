from rest_framework import filters, generics
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.utils import timezone
from django.core.files.images import ImageFile
from django.core.files import File

from .forms import *
from .models import Image as ImageModel
from .serializers import *

# Create your views here.

class Upload(APIView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        form = ImageForm()
        return render(request, 'upload.html', {'form': form})

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            new_image = Image(
                base_image=form.cleaned_data['base_image'],
                datetime=timezone.now()
            )
            new_image.save()
            new_image.treatment()
            new_image.save()

            return JsonResponse({'message': 'success'})

        return JsonResponse({'message': 'error'})

class Images(generics.ListAPIView):
    serializer_class = ImageSerializer
    query_limit = 10

    def get_queryset(self):
        # If no from_id GET parameter, queries the last "query_limit" images
        queryset = ImageModel.objects.order_by('-id')[:self.query_limit]
        from_id = self.request.query_params.get('from_id', None)
        if from_id is not None:
            # If from_id GET parameter, queries "query_limit" images from the given id
            queryset = ImageModel.objects.filter(id__lt=from_id).order_by('-id')[:self.query_limit]
        return queryset

class Image(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
