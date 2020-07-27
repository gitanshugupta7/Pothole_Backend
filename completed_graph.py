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

def export_data_completed():

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


    for data in pothole_overall_data:
        for i,j in statistics_final.items():
            for k in j:
                if(k==data.ward_no):
                    j[k]['complaints_registered']= pothole.objects.filter(ward_no=k,status='Recent').count() + pothole.objects.filter(ward_no=k, status='Ongoing').count()
                    j[k]['complaints_completed'] = pothole.objects.filter(ward_no=k, status='Completed').count()
       

    series=list()
    temp = dict()
    final_list = list()
    temp_2 = dict()
    for key,val in statistics_final.items():
        for i in val:
            temp['name'] = i
            temp_2['name'] = key
            if(type(val[i]['complaints_registered']) is int):
                temp_2['value'] = val[i]['complaints_registered']
            else:
                temp_2['value'] = 0
            series.append(temp_2)
            temp_2 = dict()
            temp['series'] = series
            series = list()
            final_list.append(temp)
            temp = dict()

    l = list()
    tempo = dict()
    print(len(final_list))
    for i in range(0,len(final_list)-1):
        for j in range(i+1,len(final_list)):
            if(final_list[j]['name'] == final_list[i]['name']):
                tempo['name'] = final_list[j]['series'][0]['name']
                tempo['value'] = final_list[j]['series'][0]['value']
                final_list[i]['series'].append(tempo)
                tempo = dict()
                l.append(j)

    #print(len(l))
    #print(l[0])
    #print(l[len(l)])
    del final_list[l[0]:l[len(l)-1]]
    #print(len(final_list))
    del final_list[(len(final_list)-1)]

    return final_list





