from django.shortcuts import render
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
import datetime
import emoji
import random
import json
import wget
import urllib
import urllib3
import shutil
from urllib.request import urlopen
import os
import uuid


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
import django
django.setup()

from app1.models import whatsapp_data, pothole

def give_stats(request):

    resp = MessagingResponse()
    msg = resp.message()

    account_sid = 'ACe57983b4051b116e6a61919f585d772d'
    auth_token = 'bc9b19d1f67dd2e493e159d5355b6d44'

    pothole_recent_data = pothole.objects.filter(status='Recent')
    pothole_ongoing_data = pothole.objects.filter(status='Ongoing')
    pothole_completed_data = pothole.objects.filter(status='Completed')

    whatsapp = whatsapp_data.objects.all()

    recents_count = 0
    recents_address = list()
    recents_time = list()
    ongoing_count = 0
    ongoing_address = list()
    ongoing_time = list()
    completed_count = 0
    completed_address = list()
    completed_time = list()

    user_phone = str(request.POST['From'])[9:]

    for data1 in whatsapp:
        if(data1.number == user_phone):
            for data2 in pothole_recent_data:
                if(data2.complaint_id == data1.complaint_id):
                    recents_count += 1
                    recents_address.append(data2.address)
                    recents_time.append(data2.uploaded_timestamp)
            for data3 in pothole_ongoing_data:
                if(data3.complaint_id == data1.complaint_id):
                    ongoing_count += 1
                    ongoing_address.append(data3.address)
                    ongoing_time.append(data3.uploaded_timestamp)
            for data4 in pothole_completed_data:
                if(data4.complaint_id == data1.complaint_id):
                    completed_count += 1
                    completed_address.append(data4.address)
                    completed_time.append(data4.uploaded_timestamp)

    client = Client(account_sid, auth_token)
    t = str(timezone.now())
    total = recents_count + ongoing_count + completed_count
    response = emoji.emojize("""
Dear user , this is to inform that """

+"""Till"""+t[:19]+

"""You have reported total """+str(total)+""" potholes"""

+"""*Recently*"""+

"""You have reported """+str(recents_count)+""" potholes"""+

"""Report details :"""+
"""Reported at : """+str(recents_address[0])

+"""Reporting time : """+str(recents_time[0])[:19] 
, use_aliases=True)
    message = client.messages \
        .create(
            from_='whatsapp:+14155238886',
            body= response,
            to=request.POST['From']
            )
