from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

import os
from django.conf import settings
from .forms import *
from .models import Image

# Create your views here.

class Home(APIView):

    def get(self, request, *args, **kwargs):
        form = ImageForm()
        return render(request, 'home.html', {'form' : form})
        

class Upload(APIView): 

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES) 

        if form.is_valid():
            image = form.save()
            image.processed_image = image.all()
            image.save()

            return HttpResponse('Success !')

        return HttpResponseNotFound('Error...')
