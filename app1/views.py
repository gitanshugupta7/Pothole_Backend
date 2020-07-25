from . models import pothole
from . serializers import PotholeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import json
import datetime
import emoji
import random
from microinformation import MIS
from points_distance import coordinates_distance

class MISData(APIView):

    def get(self, request, ward):
        mis_data = MIS(ward)
        return Response(mis_data)

    def post(self, request):
        pass
        
class Pothole(APIView):

    def Convert(self,lst): 
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
        return res_dct 
    
    def get_key(self,val,my_dict): 
        for key, value in my_dict.items(): 
             if val == value: 
                 return key 
  
        return "key doesn't exist"
    
    def get(self, request, ward, st, format=None):
        pothole_data = pothole.objects.filter(status=st, ward_no=ward)
        serializer = PotholeSerializer(pothole_data, many=True)
        l1 = list()
        l2 = list()
        l5 = list()
        l6 = list()
        for i in pothole_data:
            l1.append(i.complaint_id)
            l1.append(i.coordinates)
            l2.append(i.coordinates)
        key_dict = self.Convert(l1)
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
                        id_to_increment = self.get_key(l2[i],key_dict)
                        print("Id to increment is :",id_to_increment)
                        id_to_delete = self.get_key(l2[j],key_dict)
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
        return Response(serializer.data)

    def post(self, resquest, st, format=None):
        pothole = pothole.objects.all()
        pothole.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PotholeDetails(APIView):
    
    def get_object(self, st):
        try:
            return pothole.objects.get(complaint_id=st)
        except pothole.DoesNotExist:
            raise Http404
    
    def get(self, request, st, format=None):
        pothole = self.get_object(st)
        serializer = PotholeSerializer(pothole)
        return Response(serializer.data)

    def put(self, request, st, format=None):
        data = json.loads(request.body)
        pothole = self.get_object(st)

        if data['status'] == 'Ongoing' :
            pothole.ongoing_timestamp = timezone.now()

        if data['status'] == 'Completed':
            pothole.completed_timestamp = timezone.now()

        serializer = PotholeSerializer(pothole, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, st, format=None):
        pothole = self.get_object(st)
        pothole.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
