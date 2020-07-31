from django.shortcuts import render
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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

def feedback():

    #print("Feedback in progress\n\n")

    resp = MessagingResponse()
    msg = resp.message()

    account_sid = 'ACe57983b4051b116e6a61919f585d772d'
    auth_token = 'bc9b19d1f67dd2e493e159d5355b6d44'

    responded = False

    pothole_data = pothole.objects.filter(status='Ongoing')

    whatsapp = whatsapp_data.objects.all()

    for data1 in pothole_data:
        if(data1.feedback_flag == 'Registered'):
            if(data1.no_of_reporters > 1):
                id_list = list()
                id_list.append(data1.complaint_id)
                data = len(str(data1.complaint_id_duplicate))
                if(data>36):
                    temp = str(data1.complaint_id_duplicate).split(',')
                    for j in len(temp):
                        id_list.append(temp[j])
                    temp = list()
                else:
                    id_list.append(data1.complaint_id_duplicate)
                for i in range(len(id_list)):
                    for data2 in whatsapp:
                        if(data2.complaint_id == id_list[i]):
                            phone = 'whatsapp:'+str(data2.number)
                            client = Client(account_sid, auth_token)

                            response = emoji.emojize("""
This is to inform that in reference to your complaint id """

+str(id_list[i])+
"""\n\nReported from :\n\n"""
+str(data1.address)+
"""\n\nWard Number : """+str(data1.ward_no)+
"""\n\nAt : """+str(data1.uploaded_timestamp)[:19]+

"""
\n\n*Repair work has started* :man_mechanic: :man_construction_worker:


You will again be notified once the repair work is finished :thumbs_up::fire::fire:
""", use_aliases=True)
                            message = client.messages \
                                .create(
                                    from_='whatsapp:+14155238886',
                                    body= response,
                                    to=phone
                                )

                responded = True
                data1.feedback_flag = "Notified On Repair Start"
                data1.save()
                id_list = list()
                print("Feedback sent\n\n")

            if(data1.no_of_reporters == 1):
                id_list = data1.complaint_id
                for data2 in whatsapp:
                    if(data2.complaint_id == id_list):
                        phone = 'whatsapp:'+str(data2.number)
                        client = Client(account_sid, auth_token)

                        response = emoji.emojize("""
This is to inform that in reference to your complaint id """

+str(id_list)+
"""\n\nReported from :\n\n"""
+str(data1.address)+
"""\n\nWard Number : """+str(data1.ward_no)+
"""\n\nAt : """+str(data1.uploaded_timestamp)[:19]+

"""
\n\n*Repair work has started* :man_mechanic: :man_construction_worker:


You will again be notified once the repair work is finished :thumbs_up::fire::fire:
""", use_aliases=True)
                        message = client.messages \
                            .create(
                                from_='whatsapp:+14155238886',
                                body= response,
                                to=phone
                            )

                responded = True
                data1.feedback_flag = "Notified On Repair Start"
                data1.save()
                id_list = list()
                print("Feedback sent\n\n")


    pothole_completed_data = pothole.objects.filter(status='Completed')

    for data1 in pothole_completed_data:
        if(data1.feedback_flag == 'Notified On Repair Start'):
            if(data1.no_of_reporters > 1):
                id_list = list()
                id_list.append(data1.complaint_id)
                data = len(str(data1.complaint_id_duplicate))
                if(data>36):
                    temp = str(data1.complaint_id_duplicate).split(',')
                    for j in len(temp):
                        id_list.append(temp[j])
                    temp = list()
                else:
                    id_list.append(data1.complaint_id_duplicate)
                for i in range(len(id_list)):
                    for data2 in whatsapp:
                        if(data2.complaint_id == id_list[i]):
                            phone = 'whatsapp:'+str(data2.number)
                            client = Client(account_sid, auth_token)

                            response = emoji.emojize("""
This is to inform that in reference to your complaint id """

+str(id_list[i])+
"""\n\nReported from :\n\n"""
+str(data1.address)+
"""\n\nWard Number : """+str(data1.ward_no)+
"""\n\nAt : """+str(data1.uploaded_timestamp)[:19]+

"""
*Repair work has been completed* :fire:

You can further lodge complaints in the same way as you have done :fire::fire:
""", use_aliases=True)
                            message = client.messages \
                                .create(
                                    from_='whatsapp:+14155238886',
                                    body= response,
                                    to=phone
                                )

                responded = True
                data1.feedback_flag = "Notified On Completion"
                data1.save()
                id_list = list()
                print("Feedback sent\n\n")

            if(data1.no_of_reporters == 1):
                id_list = data1.complaint_id
                for data2 in whatsapp:
                    if(data2.complaint_id == id_list):
                        phone = 'whatsapp:'+str(data2.number)
                        client = Client(account_sid, auth_token)

                        response = emoji.emojize("""
This is to inform that in reference to your complaint id\n\n"""

+str(id_list)+
"""\n\nReported from :\n\n"""
+str(data1.address)+
"""\n\nWard Number : """+str(data1.ward_no)+
"""\n\nAt : """+str(data1.uploaded_timestamp)[:19]+
"""
\n\n*Repair work has been completed* :fire:

You can further lodge complaints in the same way as you have done :fire::fire:
""", use_aliases=True)
                        message = client.messages \
                            .create(
                                from_='whatsapp:+14155238886',
                                body= response,
                                to=phone
                            )

                responded = True
                data1.feedback_flag = "Notified On Completion"
                data1.save()
                id_list = list()
                print("Feedback sent\n\n")
