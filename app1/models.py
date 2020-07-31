from django.db import models
from django.utils import timezone


class twitter_data(models.Model):
    complaint_id = models.CharField(max_length=64, default='', blank='True')
    tweet_id = models.CharField(max_length=256, default='', blank='True')
    name = models.CharField(max_length=128, default='', blank='True')
    username = models.CharField(max_length=128, default='', blank='True')

    def __str__(self):
        return self.complaint_id


class whatsapp_data(models.Model):
    complaint_id = models.CharField(max_length=64, default='', blank='True')
    number = models.CharField(max_length=256, default='', blank='True')
    name = models.CharField(max_length=128, default='', blank='True')
  
    def __str__(self):
        return self.complaint_id
    
         
class pothole(models.Model):
    complaint_id = models.CharField(max_length=3000, default='', blank='True')
    coordinates = models.CharField(max_length=64, default='', blank='True') 
    address = models.CharField(max_length=512, default='', blank='True')
    status = models.CharField(max_length=20, default='Recent')
    uploaded_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    ongoing_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    completed_timestamp = models.DateTimeField(default=timezone.now, blank=True)
    ward_no = models.IntegerField(default=108)
    no_of_reporters = models.IntegerField(default=1)
    pothole_image = models.ImageField(upload_to = "pothole_pictures", blank = "True")
    origin = models.CharField(max_length=32, default='', blank='True')
    feedback_flag = models.CharField(max_length=25, default='Registered')

    

   