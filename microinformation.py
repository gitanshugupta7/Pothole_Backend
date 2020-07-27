
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
import django
django.setup()
from datetime import datetime
from pytz import timezone
import json

from app1.models import pothole
from app1.serializers import PotholeSerializer

statistics_final = dict()
attributes = ['complaints_registered','complaints_completed']

def MIS(wd):

    final = dict()
    
    final['all_count'] = pothole.objects.filter(status='Recent').count()
    final['particular'] = pothole.objects.filter(ward_no=wd).count()

    final['completed'] = pothole.objects.filter(ward_no=wd, status='Completed').count()
    completed = pothole.objects.filter(ward_no=wd, status='Completed').count()
    final['ongoing'] = pothole.objects.filter(ward_no=wd, status='Ongoing').count()
    ongoing = pothole.objects.filter(ward_no=wd, status='Ongoing').count()
    final['registered'] = pothole.objects.filter(ward_no=wd,status='Recent').count() + pothole.objects.filter(ward_no=wd, status='Ongoing').count()
    final['recent'] = pothole.objects.filter(ward_no=wd, status='Recent').count()

    pothole_completed = pothole.objects.filter(ward_no=wd, status='Completed')
    pothole_ongoing = pothole.objects.filter(ward_no=wd, status='Ongoing')
    avg_days = 0.0
    avg_days2 = 0.0
             
    #print(statistics_final)
    
    # graph.plotting(statistics_final)

    for i in pothole_completed:
        avg_days = (avg_days + (i.ongoing_timestamp - i.completed_timestamp).days)
        
    
    for i in pothole_ongoing:
        avg_days2 = (avg_days2 + (i.uploaded_timestamp - i.ongoing_timestamp).days)
        
    # final['avg_completed'] = avg_days/completed
    # final['avg_ongoing'] = avg_days2/ongoing 

    print(final)

    return final
    