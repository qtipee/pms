from django.db import models
import os

# Create your models here.

class Image(models.Model):

    def base_image_directory(instance, filename):
        # File will be uploaded to MEDIA_ROOT/samples/<username>/<sample_name>
        name, ext = os.path.splitext(filename)
        return 'images/{0}-base{1}'.format(name, ext)

    def processed_image_directory(instance, filename):
        # File will be uploaded to MEDIA_ROOT/samples/<username>/<sample_name>
        name, ext = os.path.splitext(filename)
        return 'images/{0}-processed{1}'.format(name, ext)

    base_image = models.ImageField(max_length=255, upload_to=base_image_directory)
    processed_image = models.ImageField(max_length=255, upload_to=processed_image_directory, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
