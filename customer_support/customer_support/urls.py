from django.contrib import admin
from django.urls import path

from customer_support.views import trigger_complaint_event, trigger_ticket_event

urlpatterns = [path("admin/", admin.site.urls), path("trigger/", trigger_ticket_event)]
