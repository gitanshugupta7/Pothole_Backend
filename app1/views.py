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

class Pothole(APIView):
    
    def get(self, request, ward, st, format=None):
        pothole_data = pothole.objects.filter(status=st, ward_no=ward)
        serializer = PotholeSerializer(pothole_data, many=True)
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
