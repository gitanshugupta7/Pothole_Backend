from rest_framework import serializers
from . models import pothole
    

class PotholeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = pothole
		fields = "__all__"
    

