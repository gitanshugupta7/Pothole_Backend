
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
import django
django.setup()
from datetime import datetime
from pytz import timezone
import json


from app1.models import pothole
from app1.serializers import PotholeSerializer

def MIS(st):

    final = dict()
    
    final['all_count'] = pothole.objects.all().count()
    final['particular'] = pothole.objects.filter(ward_no=st).count()

    final['completed'] = pothole.objects.filter(ward_no=st, status='Completed').count()
    completed = pothole.objects.filter(ward_no=st, status='Completed').count()
    final['ongoing'] = pothole.objects.filter(ward_no=st, status='Ongoing').count()
    ongoing = pothole.objects.filter(ward_no=st, status='Ongoing').count()
    final['registered'] = pothole.objects.filter(ward_no=st, status='Recent').count() + pothole.objects.filter(ward_no=st, status='Ongoing').count()

    pothole_completed = pothole.objects.filter(ward_no=st, status='Completed')
    pothole_ongoing = pothole.objects.filter(ward_no=st, status='Ongoing')
    avg_days = 0.0
    avg_days2 = 0.0

    for i in pothole_completed:
        avg_days = (avg_days + (i.ongoing_timestamp - i.completed_timestamp).days)
    
    for i in pothole_ongoing:
        avg_days2 = (avg_days2 + (i.uploaded_timestamp - i.ongoing_timestamp).days)
        
    final['avg_completed'] = avg_days/completed
    final['avg_ongoing'] = avg_days2/ongoing 

    final_json = json.dumps(final) 

    return final_json
    

MIS(108)