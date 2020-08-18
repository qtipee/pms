import os
import mimetypes
from rest_framework import filters, generics
from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.conf import settings
from django.utils import timezone
from django.core.files.images import ImageFile
from django.core.files import File

from .forms import *
from .models import Image as ImageModel
from .serializers import *

# Create your views here.


class Upload(APIView):

    def get(self, request, *args, **kwargs):
        '''
        Upload image form (for web browser access)
        '''
        form = ImageForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request, *args, **kwargs):
        '''
        Upload an image file
        '''
        try:
            image_file = request.FILES['base_image']
            filename = image_file.name
            path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
            with open(path, 'wb') as img:
                # Writes the uploaded image in MEDIA_ROOT/images
                for b in image_file:
                    img.write(b)

            return JsonResponse({'message': 'Image successfully uploaded !', 'filename': filename}, status=200)
        except Exception as error:
            return JsonResponse({'error': str(error), 'post': str(request.data)}, status=400)


class Process(APIView):
    def get(self, request, filename):
        '''
        Processes the image associated to the given filename
        '''
        try:
            path = os.path.join(settings.MEDIA_ROOT, 'images', filename)
            new_image = ImageModel(
                base_image=File(open(path, 'rb')),
                datetime=timezone.now()
            )
            new_image.count_grap()  # Image processing
            new_image.save()  # Saves the model in the database

            os.remove(path)  # Removes the temporary uploaded image file

            return JsonResponse({'message': 'Image successfully processed !'}, status=200)
        except Exception as error:
            return JsonResponse({'error': str(error), 'post': str(request.data)}, status=400)


class Images(generics.ListAPIView):
    '''
    To get multiple images models
    '''
    serializer_class = ImageSerializer
    query_limit = 10

    def get_queryset(self):
        # If no from_id GET parameter, queries the last "query_limit" images
        queryset = ImageModel.objects.order_by('-id')[:self.query_limit]
        from_id = self.request.query_params.get('from_id', None)
        if from_id is not None:
            # If from_id GET parameter, queries "query_limit" images from the given id
            queryset = ImageModel.objects.filter(
                id__lt=from_id).order_by('-id')[:self.query_limit]
        return queryset


class Image(generics.RetrieveAPIView):
    '''
    To get a single image model (by id)
    '''
    lookup_field = 'id'
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer


class ImageFile(APIView):
    '''
    To get an image file
    '''

    def get(self, request, image_id, image):
        # Image model contains two images : base_image and processed_image
        if image == 'base' or image == 'processed':
            image += '_image'
            file = ImageModel.objects.filter(id=image_id).values(image).get()

            if file:
                path_to_file = os.path.join(settings.MEDIA_ROOT, file[image])
                with open(path_to_file, 'rb') as image_file:
                    # Prepares the image file for HTTP request
                    mime_type = mimetypes.MimeTypes(
                    ).guess_type(file[image][0])
                    response = HttpResponse(image_file, content_type=mime_type)
                    filename = file[image].split('/')[-1]
                    response['Content-Disposition'] = f'attachement; filename="{filename}"'

                return response

        return HttpResponseNotFound('No matching file found.')


class ImageCountUpdate(APIView):

    def get(self, request, image_id, count):
        '''
        Updates the count property of the image model associated to the given id
        '''
        try:
            image = ImageModel.objects.filter(id=image_id).get()
            image.count = count
            image.save()

            return JsonResponse({'message': 'Image count successfully updated !'}, status=200)
        except Exception as error:
            return JsonResponse({'error': str(error)}, status=400)
