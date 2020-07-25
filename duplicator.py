from . models import pothole
from . serializers import PotholeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import json
import datetime
import random
from microinformation import MIS
from points_distance import coordinates_distance

def Convert(lst): 
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
        return res_dct 
    
def get_key(val,my_dict): 
    for key, value in my_dict.items(): 
        if val == value: 
            return key 
  
    return "key doesn't exist"

def duplicate_check(st,ward):
    pothole_data = pothole.objects.filter(status=st, ward_no=ward)
    l1 = list()
    l2 = list()
    l5 = list()
    l6 = list()
    for i in pothole_data:
        l1.append(i.complaint_id)
        l1.append(i.coordinates)
        l2.append(i.coordinates)
    key_dict = Convert(l1)
    for i in l2:
        l4 = i.split(',')
        l5.append(float(l4[0]))
        l5.append(float(l4[1]))
        t = tuple(l5)
        l6.append(t)
        l5 = []
    delete_status = list()
    for i in range(len(l6)):
        delete_status.append(0)
    for i in range(0,len(l6)-1):
        for j in range(i+1,len(l6)):
            if(delete_status[j]==0):
                distance = coordinates_distance(l6[i],l6[j])
                print("Distance between ",i," and ",j," is ",distance)
                if(distance<=20.0):
                    id_to_increment = get_key(l2[i],key_dict)
                    print("Id to increment is :",id_to_increment)
                    id_to_delete = get_key(l2[j],key_dict)
                    print("Id to delete is : ",id_to_delete)
                    delete_status[j] = 1
                    for k in pothole_data:
                        if(k.complaint_id==id_to_increment):
                            k.no_of_reporters += 1
                            k.complaint_id = str(k.complaint_id)+','+str(id_to_delete)
                        k.save()
                    for k in pothole_data:
                        if(k.complaint_id==id_to_delete):
                            k.delete()
    print("\nDuplicate check done\n")