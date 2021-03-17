from django.db import models 

# Create your models here.
from django.contrib import admin

class Abnormal_Image(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/abnormal_image")
    
    def __unicode__(self):
        return self.image.name
    
    def save_image(self, image):
        self.image = image

class Abnormal_Image_Admin(admin.ModelAdmin):
    list_display = ('image', 'timestamp')

