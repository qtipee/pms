from rest_framework.views import APIView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.utils import timezone

from .models import *
from .forms import *

# Create your views here.

class Upload(APIView):

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        form = ImageForm()
        return render(request, 'upload.html', {'form' : form})

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            new_image = Image(
                base_image=form.cleaned_data['base_image'],
                datetime=timezone.now()
            )
            new_image.save()

            return JsonResponse({ 'message': 'success' })

        return JsonResponse({ 'message': 'error' })
