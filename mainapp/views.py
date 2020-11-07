# coding: utf-8

import sys

from io import BytesIO
from PIL import Image

from django.template.context_processors import csrf
from django.views.generic import TemplateView
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from django.conf import settings

from .models import ImageStore
from .serializers import ImageSerializer


class MainView(TemplateView):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context.update(csrf(request))
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['media'] = settings.MEDIA_URL
        context['images'] = ImageStore.objects.all()
        print(dir(context['images'][0]))
        return context


class ImageList(ListAPIView,
                CreateAPIView,
                DestroyAPIView):
    queryset = ImageStore.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        self.pk = None
        super(ImageList, self).__init__(**kwargs)

    def get_queryset(self):
        if not self.pk:
            return super(ImageList, self).get_queryset()
        else:
            return ImageStore.objects.filter(pk=self.pk)

    def create(self, request, *args, **kwargs):
        for i in request.FILES:
            obj = ImageStore.objects.create(image=request.FILES[i])
            img = Image.open(obj.image.path)
            img = img.convert('RGB')
            img.thumbnail((128, 128), Image.ANTIALIAS)
            thumb_io = BytesIO()
            f = 'JPEG'
            if request.FILES[i].name.split('.')[-1].lower() == 'png':
                f = 'PNG'
            img.save(thumb_io, format=f)
            obj.image_mini = InMemoryUploadedFile(thumb_io, None, obj.image.path, 'image/jpeg',
                                                  img.tell, None)
            obj.save()
        return Response(ImageSerializer(obj).data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        if request.query_params.get('pk', None):
            self.pk = request.query_params.get('pk')
        return super(ImageList, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        ImageStore.objects.get(pk=request.query_params.get('pk')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
