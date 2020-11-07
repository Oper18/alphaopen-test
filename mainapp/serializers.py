# coding: utf-8

from PIL import Image

from django.conf import settings

from rest_framework import serializers

from .models import ImageStore


class ImageSerializer(serializers.ModelSerializer):
    resolution = serializers.SerializerMethodField('get_resolution')
    size = serializers.SerializerMethodField('get_size')
    extension = serializers.SerializerMethodField('get_extension')
    image_path = serializers.SerializerMethodField('get_image_path')
    image_mini_path = serializers.SerializerMethodField('get_image_mini_path')

    class Meta:
        model = ImageStore
        fields = ['id', 'image', 'image_mini', 'resolution', 'size', 'extension', 'image_path', 'image_mini_path']

    def get_resolution(self, obj):
        return obj.image.size

    def get_size(self, obj):
        return 'x'.join([str(i) for i in Image.open(obj.image.path).size])

    def get_extension(self, obj):
        try:
            return obj.image.path.split('.')[-1]
        except:
            return None

    def get_image_path(self, obj):
        return obj.image.url

    def get_image_mini_path(self, obj):
        return obj.image_mini.url if obj.image_mini else ''
