from django.contrib import admin

# Register your models here.

from .models import DailyStock

admin.site.register(DailyStock)
