from django.contrib import admin
from django.urls import path

from customer_support.views import trigger_product_event

urlpatterns = [path("admin/", admin.site.urls), path("trigger/", trigger_product_event)]
