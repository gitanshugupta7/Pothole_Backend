
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
import django
django.setup()
from datetime import datetime
from pytz import timezone
import json
import graph

from app1.models import pothole
from app1.serializers import PotholeSerializer

statistics_final = dict()
attributes = ['complaints_registered','complaints_completed']

def MIS(wd):

    final = dict()
    global statistics_final
    global attributes
    l = list()
    wardlist = list()
    
    for i in range(142):
        wardlist.append(i)

    pothole_overall_data = pothole.objects.filter(status='Recent')
    for i in pothole_overall_data:
        temp = str(i.uploaded_timestamp)
        key = temp[:10]
        if key not in statistics_final.keys():
            l.append(key)
            statistics_final[key] = dict.fromkeys(wardlist)
            l=[]

    for i,j in statistics_final.items():
        for k in j:
            j[k] = dict.fromkeys(attributes)
    
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

    for data in pothole_overall_data:
        for i,j in statistics_final.items():
            for k in j:
                if(k==data.ward_no):
                    j[k]['complaints_registered']= pothole.objects.filter(ward_no=k,status='Recent').count() + pothole.objects.filter(ward_no=k, status='Ongoing').count()
                    j[k]['complaints_completed'] = pothole.objects.filter(ward_no=k, status='Completed').count()
                    
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
    