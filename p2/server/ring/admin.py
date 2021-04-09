from django.contrib import admin

# Register your models here.
from .models import (
    Abnormal_Image, Abnormal_Image_Admin
)

admin.site.register(Abnormal_Image, Abnormal_Image_Admin)

