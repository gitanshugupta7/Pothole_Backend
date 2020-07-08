from . models import pothole
from . serializers import PotholeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Pothole(APIView):

    def get(self, request, format=None):
        pothole_data = pothole.objects.all()
        serializer = PotholeSerializer(pothole_data, many=True)
        return Response(serializer.data)

    def post(self, resquest, format=None):
        pass

class PotholeDetails(APIView):
    
    def get_object(self, pk):
        try:
            return pothole.objects.get(pk=pk)
        except pothole.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        pothole = self.get_object(pk)
        serializer = PotholeSerializer(pothole)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        pothole = self.get_object(pk)
        serializer = PotholeSerializer(pothole, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        pothole = self.get_object(pk)
        pothole.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


