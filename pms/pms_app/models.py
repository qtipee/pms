from django.db import models
import os

# Create your models here.

class Image(models.Model):

    def base_image_directory(instance, filename):
        # File will be uploaded to MEDIA_ROOT/images/<date>/<time>-base.<ext>
        ext = os.path.splitext(filename)[1]
        return 'images/{0}/{1}_base{2}'.format(instance.datetime.date(), instance.datetime.time(), ext)

    def processed_image_directory(instance, filename):
        # File will be uploaded to MEDIA_ROOT/images/<date>/<time>-processed.<ext>
        ext = os.path.splitext(filename)[1]
        return 'images/{0}/{1}_processed{2}'.format(instance.datetime.date(), instance.datetime.time(), ext)

    base_image = models.ImageField(max_length=255, upload_to=base_image_directory)
    processed_image = models.ImageField(max_length=255, upload_to=processed_image_directory, blank=True)
    datetime = models.DateTimeField(blank=True)
