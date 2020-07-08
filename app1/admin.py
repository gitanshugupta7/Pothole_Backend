from django.contrib import admin
from . models import pothole, complaint, twitter_data
# Register your models here.


admin.site.register(pothole)
admin.site.register(complaint)
admin.site.register(twitter_data)