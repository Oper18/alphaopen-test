# coding: utf-8

from django.urls import re_path

from .views import MainView, ImageList

urlpatterns = [
    re_path(r'^$', MainView.as_view(template_name='mainapp/index.html'), name='main'),
    re_path(r'^api/images/$', ImageList.as_view()),
]
