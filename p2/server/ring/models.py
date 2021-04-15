from django.db import models 

# Create your models here.
from django.contrib import admin

import uuid
from datetime import datetime
from django.contrib.auth.models import AbstractUser


#################################################################
############################  Model  ############################

# User
class User(models.Model):
    name = models.CharField(max_length=100, default=None)
    passwd = models.CharField(max_length=100, default=None)

# Version
class Version(models.Model):
    abstract = models.TextField(max_length=1000, default=None)
    git_repo = models.CharField(max_length=500, default=None)
    git_version = models.CharField(max_length=50, default=None)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.abstract 
    def __str__(self):
        return f"{str(self.git_repo).split('/')[-1]} ({str(self.git_version)})"

# Device
class Device(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    nick_name = models.CharField(max_length=50, default=None)
    mac_addr = models.CharField(max_length=200, default=None)
    alive = models.BooleanField(default=False)
    latest_check = models.TimeField(auto_now_add=True) #最近的握手
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    update_to_version = models.ForeignKey(Version, on_delete=models.CASCADE,
                                related_name='%(class)s_requests_created')
    keep_newest = models.BooleanField(default=False)
    def __str__(self):
        return str(self.uid)
    def __unicode__(self):
        return self.uid 

# Knock
class Knock(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

# Unlock
class Unlock(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

# Version Log
class VersionLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return f"{self.device}_{self.version}_{self.timestamp}"

# Cookie
class Cookie(models.Model):
    sessionid = models.CharField(max_length=200, default=None)
    last_login = models.DateTimeField(auto_now_add=True)
    #device = models.ForeignKey(Device, on_delete=models.CASCADE, default=None)

# Abnormal Images
class Abnormal_Image(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/abnormal_image")
    
    def __unicode__(self):
        return self.image.name
    
    def save_image(self, image):
        self.image = image


#################################################################
############################  Admin  ############################

class User_Admin(admin.ModelAdmin):
    list_display = ('name', 'passwd')

class Version_Admin(admin.ModelAdmin):
    list_display = ('git_repo', 'git_version', 'abstract', 'timestamp')

class Device_Admin(admin.ModelAdmin):
    #fields = ('mac_addr', ('version','update_to_version'), 'keep_newest')
    
    fieldsets = (
        (None, {'fields': ('uid', 'mac_addr', 'nick_name')}),
        ('Version Control', {'fields': (('version', 'update_to_version'), 'keep_newest')})
    )
    
    search_fields = ('uid', 'nick_name', 'version__git_repo', 'version__git_version')
    list_display = ('nick_name', 'uid', 'mac_addr', 'alive', 'latest_check', 'version', 
                    'update_to_version', 'keep_newest')
    list_display_links = ('uid','mac_addr', 'version')
    ordering = ('-latest_check', 'mac_addr')
    list_filter = ('alive', 'latest_check', 'version', 'keep_newest')
    list_select_related = ('version',)
    #actions
    actions = ['make_keep_newest', 'keep_old_version']
    def make_keep_newest(self, request, queryset):
        queryset.update(keep_newest=True)
    def keep_old_version(self, request, queryset):
        queryset.update(keep_newest=False)
    make_keep_newest.short_description = "keep newest version"
    keep_old_version.short_description = "keep old version"

class VersionLog_Admin(admin.ModelAdmin):
    list_display = ('device', 'version', 'timestamp')
    list_filter = ('version',)

class Abnormal_Image_Admin(admin.ModelAdmin):
    list_display = ('image', 'timestamp')

class Cookie_Admin(admin.ModelAdmin):
    list_display = ('sessionid', 'last_login')

