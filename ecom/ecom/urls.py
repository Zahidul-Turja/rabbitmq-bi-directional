from django.contrib import admin
from django.urls import path
from .view import trigger

urlpatterns = [path("admin/", admin.site.urls), path("trigger/", trigger)]
