from django.contrib import admin

# Register your models here.
from .models import (
    Abnormal_Image, Abnormal_Image_Admin,
    User, User_Admin,
    Device, Device_Admin,
    Version, Version_Admin,
    VersionLog, VersionLog_Admin,
    Cookie, Cookie_Admin
)

admin.site.register(Abnormal_Image, Abnormal_Image_Admin)
admin.site.register(User, User_Admin)
admin.site.register(Device, Device_Admin)
admin.site.register(Version, Version_Admin)
#admin.site.register(VersionLog, VersionLog_Admin)
admin.site.register(Cookie, Cookie_Admin)
