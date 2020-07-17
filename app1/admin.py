from django.contrib import admin
from . models import pothole, twitter_data, whatsapp_data
# Register your models here.


admin.site.register(pothole)
admin.site.register(twitter_data)
admin.site.register(whatsapp_data)