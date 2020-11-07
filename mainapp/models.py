# coding: utf-8

from django.db import models


class ImageStore(models.Model):
    image = models.ImageField(verbose_name='Full size iamge', upload_to='full_image')
    image_mini = models.ImageField(verbose_name='Image miniature', upload_to='mini_image', null=True, blank=True)
