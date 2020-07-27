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
from bot_app import logic


@csrf_exempt
def index(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase

        print(request.POST)
        incoming_msg = request.POST['Body'].lower()
        incoming_msg = incoming_msg.strip()

        p = logic.interact(request,incoming_msg)

        return HttpResponse(p)

        