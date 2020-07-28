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
final_list_registered = list()
final_list_completed = list()

def make_data():
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

    for i,j in statistics_final.items():
        for k in j:
            j[k]['complaints_registered'] = 0
            j[k]['complaints_completed'] = 0

    for data in pothole_overall_data:
        for i,j in statistics_final.items():
            for k in j:
                if(k==data.ward_no):
                    temp = str(data.uploaded_timestamp)
                    key = temp[:10]
                    if(key == i):
                        j[k]['complaints_registered'] += 1

    pothole_completed_data = pothole.objects.filter(status='Completed')

    for data in pothole_completed_data:
        for i,j in statistics_final.items():
            for k in j:
                if(k==data.ward_no):
                    temp = str(data.uploaded_timestamp)
                    key = temp[:10]
                    if(key == i):
                        j[k]['complaints_completed'] += 1



def export_data_registered():

    global statistics_final
    global final_list_registered
    make_data()

    series=list()
    temp = dict()
    temp_2 = dict()
    for key,val in statistics_final.items():
        for i in val:
            temp['name'] = i
            temp_2['name'] = key
            temp_2['value'] = val[i]['complaints_registered']
            series.append(temp_2)
            temp_2 = dict()
            temp['series'] = series
            series = list()
            final_list_registered.append(temp)
            temp = dict()

    l = list()
    tempo = dict()
    for i in range(0,len(final_list_registered)-1):
        for j in range(i+1,len(final_list_registered)):
            if(final_list_registered[j]['name'] == final_list_registered[i]['name']):
                tempo['name'] = final_list_registered[j]['series'][0]['name']
                tempo['value'] = final_list_registered[j]['series'][0]['value']
                final_list_registered[i]['series'].append(tempo)
                tempo = dict()
                l.append(j)

    
    del final_list_registered[l[0]:l[len(l)-1]]

    del final_list_registered[(len(final_list_registered)-1)]
    l = list()

    res = [] 
    for i in range(len(final_list_registered)):
        for j in final_list_registered[i]['series']: 
            if j not in res: 
                res.append(j) 
        final_list_registered[i]['series'] = res
        res = list()


    return final_list_registered

    statistics_final = dict()
    final_list_registered = list()



def export_registered_data_for_particular_ward(wd):

    #global final_list_registered
    global statistics_final
    f = export_data_registered()
    l = list()
    for i in range(len(f)):
        if(f[i]['name'] == wd):
            l.append(f[i])
            return l
            l=list()
            statistics_final = dict()




def export_data_completed():

    global statistics_final
    global final_list_completed
    make_data()

    series=list()
    temp = dict()
    temp_2 = dict()
    for key,val in statistics_final.items():
        for i in val:
            temp['name'] = i
            temp_2['name'] = key
            temp_2['value'] = val[i]['complaints_completed']
            series.append(temp_2) 
            temp_2 = dict()
            temp['series'] = series
            series = list()
            final_list_completed.append(temp)
            temp = dict()

    l = list()
    tempo = dict()
    for i in range(0,len(final_list_completed)-1):
        for j in range(i+1,len(final_list_completed)):
            if(final_list_completed[j]['name'] == final_list_completed[i]['name']):
                tempo['name'] = final_list_completed[j]['series'][0]['name']
                tempo['value'] = final_list_completed[j]['series'][0]['value']
                final_list_completed[i]['series'].append(tempo)
                tempo = dict()
                l.append(j)

    
    del final_list_completed[l[0]:l[len(l)-1]]

    del final_list_completed[(len(final_list_completed)-1)]
    l = list()
    res = [] 
    for i in range(len(final_list_completed)):
        for j in final_list_completed[i]['series']: 
            if j not in res: 
                res.append(j) 
        final_list_completed[i]['series'] = res
        res = list()

    return final_list_completed

    statistics_final = dict()
    final_list_completed = list()




def export_completed_data_for_particular_ward(wd):

    global statistics_final
    #global final_list_completed
    p = export_data_completed()
    l = list()
    for i in range(len(p)):
        if(p[i]['name'] == wd):
            l.append(p[i])
            return l
            l=list()
            statistics_final = dict()



        
def reg_vs_complete_particular(wd):

    global statistics_final
    #global final_list_registered
    #global final_list_completed
    f = export_data_registered()
    p = export_data_completed()

    merged_list = list()
    temp = dict()

    for i in range(len(f)):
        if(f[i]['name'] == wd):
            temp['name'] = 'Registered'
            temp['series'] = f[i]['series']
            merged_list.append(temp)
            temp = dict()

    for i in range(len(p)):
        if(p[i]['name'] == wd):
            temp['name'] = 'Completed'
            temp['series'] = p[i]['series']
            merged_list.append(temp)
            temp = dict()

    return merged_list

    merged_list = list()
    statistics_final = dict()


def piedata_for_particular(wd):

    pie_list = list()
    temp = dict()

    temp['name'] = 'Registered'
    temp['value'] = pothole.objects.filter(ward_no=wd,status='Recent').count() + pothole.objects.filter(ward_no=wd, status='Ongoing').count()

    pie_list.append(temp)
    temp = dict()

    temp['name'] = 'Ongoing'
    temp['value'] = pothole.objects.filter(ward_no=wd, status='Ongoing').count()

    pie_list.append(temp)
    temp = dict()

    temp['name'] = 'Completed'
    temp['value'] = pothole.objects.filter(ward_no=wd, status='Completed').count()

    pie_list.append(temp)
    temp = dict()

    return pie_list



def piedata_for_all():

    pie_list = list()
    temp = dict()

    temp['name'] = 'Registered'
    temp['value'] = pothole.objects.filter(status='Recent').count() + pothole.objects.filter(status='Ongoing').count()

    pie_list.append(temp)
    temp = dict()

    temp['name'] = 'Ongoing'
    temp['value'] = pothole.objects.filter(status='Ongoing').count()

    pie_list.append(temp)
    temp = dict()

    temp['name'] = 'Completed'
    temp['value'] = pothole.objects.filter(status='Completed').count()

    pie_list.append(temp)
    temp = dict()

    return pie_list















