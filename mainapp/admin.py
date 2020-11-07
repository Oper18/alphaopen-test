# coding: utf-8

from django.contrib import admin

from .models import ImageStore


class ImageStoreAdmin(admin.ModelAdmin):
    pass

admin.site.register(ImageStore, ImageStoreAdmin)
