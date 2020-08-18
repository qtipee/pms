from django.db import models
import os
import cv2
import numpy as np
from django.conf import settings
import PIL.Image
from django.core.files import File
from django.core.files.images import ImageFile
from io import BytesIO

# Create your models here.
kernel = np.ones((3, 3), np.uint8)
DIST_TRANSFORM = 41.3969 * 0.5


class Image(models.Model):

    def base_image_directory(instance, filename):
        # File will be uploaded to MEDIA_ROOT/images/<date>/<time>-base.<ext>
        ext = os.path.splitext(filename)[1]
        return 'images/{0}/{1}_base{2}'.format(instance.datetime.date(), instance.datetime.time(), ext)

    def processed_image_directory(instance, filename):
        # File will be uploaded to MEDIA_ROOT/images/<date>/<time>-processed.<ext>
        ext = os.path.splitext(filename)[1]
        return 'images/{0}/{1}_processed{2}'.format(instance.datetime.date(), instance.datetime.time(), ext)

    # Database table properties for Image model
    base_image = models.ImageField(
        max_length=255, upload_to=base_image_directory)
    processed_image = models.ImageField(
        max_length=255, upload_to=processed_image_directory, blank=True)
    datetime = models.DateTimeField(blank=True)
    count = models.PositiveIntegerField(blank=True)

    def pretreatement(self):
        # Read image, filter it with otsu method and return original image and the new one
        pil_image = PIL.Image.open(self.base_image)
        img = np.array(pil_image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        return img, thresh

    def fill_hole(self, thresh):
        # Fill holes in the images
        thresh = cv2.dilate(thresh, kernel,  iterations=2)
        thresh = cv2.erode(thresh, kernel,  iterations=2)
        return thresh

    def process(self, thresh):
        # Separate different forms
        kernel = np.ones((3, 3), np.uint8)
        sure_bg = cv2.dilate(thresh, kernel, iterations=3)

        dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(
            dist_transform, DIST_TRANSFORM, 255, 0)

        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        return sure_fg, unknown

    def draw_circle(self, sure_fg, unknown, img):
        # Draw circle in the images
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers+1
        markers[unknown == 255] = 0
        markers = cv2.watershed(img, markers)
        img[markers == -1] = [255, 0, 0]

        return img, ret

    def count_grap(self):
        # Count number of grap in the base_image and save processed_image with the grap surrounded
        img, thresh = self.pretreatement()
        thresh = self.fill_hole(thresh)
        sure_fg, unknown = self.work(thresh)
        img, ret = self.draw_circle(sure_fg, unknown, img)

        self.count = ret

        img = PIL.Image.fromarray(img)
        f = BytesIO()
        img.save(f, 'JPEG')
        self.processed_image.save('test.JPG', ImageFile(f))
