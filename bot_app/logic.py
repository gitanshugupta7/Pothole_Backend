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
from potholedetector import Image
from urllib.request import urlopen
import os
import uuid
from django.utils import timezone
from shapely.geometry import shape, Point
from duplicator import duplicate_check
from bot_app import feedback_manager as fm

import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from decimal import Decimal
from geopy.geocoders import GoogleV3

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
import django
django.setup()

from app1.models import whatsapp_data, pothole

final=dict()
l = list()
l1 = ['name','media_url','latitude','longitude','address','created_at','ward_no']
count = 1

def GeoFetch(key,point):
    geocoder = GoogleV3(api_key='AIzaSyDJrBe_VguWvYK8pZhEjKd3sxituvoK2hI')
    address = geocoder.reverse(point)
    final[key]['address'] = address

def get_key(val): 
    global final
    for key, value in final.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"

def Get_Ward(my_lat,my_long):
    with open('D:/Pothole_Backend/kolkata.geojson') as f:
        js = json.load(f)

    point = Point(my_long,my_lat)

    for feature in js['features']:
        polygon = shape(feature['geometry'])
        if polygon.contains(point):
            return feature['properties']['WARD']


def interact(request,incoming_msg):
    global final
    global l
    global l1
    global count
    # create Twilio XML response
    resp = MessagingResponse()
    msg = resp.message()

    account_sid = 'AC9304409e5dd28f2e399194f0f6d92b5a'
    auth_token = 'efc5dd0418daa658fbd33a7535ac7fb9'

    fm.feedback()

    responded = False
    if incoming_msg == 'hello' or incoming_msg == 'hi':
        key = str(request.POST['From'])
        if key not in final.keys():
            l.append(key)
            final[key] = dict.fromkeys(l1) 
            l=[]
        response = emoji.emojize("""
*Hi! Welcome to Pothole Management System* :wave:
Got any complaint to lodge against potholes ?

You can give me the following commands:
:black_small_square: *'1' :* Reply 1 to lodge a complaint ! :police_car_light:

:black_small_square: *'2' :* Reply 2 to go through the instructions of lodging complaint ! :notebook:
""", use_aliases=True)
        msg.body(response)
        responded = True
        # print("\n\n",final,"\n\n")


        
    elif incoming_msg == '2':
        response = emoji.emojize("""
*The set of steps to be followed are* :

:black_small_square: *'Step 1' :* Enter your fullname in the following format : "My name is <YOUR-FULLNAME>" ! :white_heavy_check_mark:

:black_small_square: *'Step 2' :* Click a picture of the pothole and send it ! :camera:

:black_small_square: *'Step 3' :* Send your current location ! :globe_with_meridians:

Now you are ready to lodge your complaint by simply replying *'1'*.
""", use_aliases=True)
        msg.body(response)
        responded = True

        
        
    elif incoming_msg == '1':
        response = emoji.emojize("""
Enter your Fullname in the following format :

*My name is <YOUR-FULLNAME>* 
""", use_aliases=True)
        
        msg.body(response)
        responded = True


    elif incoming_msg.startswith('my name is'):
        user_name = incoming_msg[11:]
        user_name = user_name.title()
        key = str(request.POST['From'])
        if key not in final.keys():
            l.append(key)
            final[key] = dict.fromkeys(l1)
            l=[]

        final[key]['name'] = user_name
        if((final[key]['media_url'] is None) and (final[key]['address'] is None)):
            client = Client(account_sid, auth_token)
            response = emoji.emojize("""
You have successfully entered your name ! :white_heavy_check_mark:

But you have not uploaded an image of the pothole and sent your live location yet.

Upload an image of the pothole.

If you do not know how to upload an image , reply *Image* to view the steps of uploading an image on Whatsapp.

After uploading the image of the pothole , send your live location.

If you do not know how to send your live location using Whatsapp , reply *Location* to view the steps.
""", use_aliases=True)
            message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

            responded = True
            # print("\n\n",final,"\n\n")

        elif((final[key]['media_url'] is not None) and (final[key]['address'] is None)):
            client = Client(account_sid, auth_token)
            response = emoji.emojize("""
You have successfully entered your name ! :white_heavy_check_mark:

You have successfully uploaded the image of the pothole as well ! :white_heavy_check_mark:

Now , just send your live location.

If you do not know how to send your live location using Whatsapp , reply *Location* to view the steps.
""", use_aliases=True)
            message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

            responded = True
            # print("\n\n",final,"\n\n")

        elif((final[key]['media_url'] is None) and (final[key]['address'] is not None)):
            client = Client(account_sid, auth_token)
            response = emoji.emojize("""
You have successfully entered your name ! :white_heavy_check_mark:

You have successfully sent your live location as well ! :white_heavy_check_mark:

Now , just send the image of the pothole.

If you do not know how to send an image using Whatsapp , reply *Image* to view the steps.
""", use_aliases=True)
            message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

            responded = True
            # print("\n\n",final,"\n\n")

        elif((final[key]['media_url'] is not None) and (final[key]['address'] is not None)):
            client = Client(account_sid, auth_token)
            response = emoji.emojize("""
You have successfully entered your name ! :white_heavy_check_mark:

And with that you have successfully registered your complaint.
""", use_aliases=True)
            message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

            responded = True
            print("\n\n",final,"\n\n")
            #store data in model here

            whatsapp = whatsapp_data()
            whatsapp.complaint_id = final[key]['image_id']
            number = get_key(final[key])
            whatsapp.number = number[9:]
            whatsapp.name = final[key]['name']
            whatsapp.save()

            current_complaint = pothole()

            current_complaint.complaint_id = str(final[key]['image_id'])
            current_complaint.uploaded_timestamp = timezone.now()
            current_complaint.coordinates = str(final[key]['latitude'])+','+str(final[key]['longitude'])
            current_complaint.address = final[key]['address']
            current_complaint.pothole_image = str(final[key]['image_id'])+'.jpg'
            current_complaint.ward_no = int(final[key]['ward_no'])
            current_complaint.origin = 'whatsapp'
            current_complaint.save()

            duplicate_check('Recent',final[key]['ward_no'])

            del final[key]
        

    elif incoming_msg == 'image':
        
        client = Client(account_sid, auth_token)

        response = emoji.emojize("""
*Have a look at the image and follow the instructions carefully*

:black_small_square: *'Step 1' :* Firstly you can click on the camera button to the right of the chatbox. Secondly , you can also click on the attachment pin to the left of camera button , a display will open as shown in the image , select "Camera" or "Gallery" from the display.


:black_small_square: *'Step 2' :* This will open the camera. Here you can either take the picture of the pothole or select the picture from your phone gallery.


:black_small_square: *'Step 3' :* The picture selected or shot will then be immediately sent.


If you have understood the instructions , reply *AR*.
""", use_aliases=True)
        message = client.messages \
            .create(
                from_='whatsapp:+14155238886',
                body= response,
                media_url = 'https://api.twilio.com/2010-04-01/Accounts/AC9304409e5dd28f2e399194f0f6d92b5a/Messages/MM11dea5cc736058a85ee29ec812291708/Media/MEe84be185eb89bbc25a8dbee7e3de68b8',
                to=request.POST['From']
            )

        responded = True


    elif incoming_msg == 'ar':
        response = emoji.emojize("""
Upload an image of the pothole , following the given instructions ! :outbox_tray:

""", use_aliases=True)
        msg.body(response)
        responded = True


    elif 'MediaContentType0' in request.POST.keys():
        image_url = request.POST['MediaUrl0']
        key = str(request.POST['From'])
        if key not in final.keys():
            l.append(key)
            final[key] = dict.fromkeys(l1)
            l=[]


        final[key]['image_id'] = str(uuid.uuid4())
        resp1 = requests.get(image_url, stream=True)
        local_file = open("D:/Pothole_Backend/media/"+ str(final[key]['image_id']) + ".jpg", 'wb')
        resp1.raw.decode_content = True
        shutil.copyfileobj(resp1.raw, local_file)
        del resp1
        unique_id = str(final[key]['image_id'])
        punk = Image(unique_id)
        # print("Predicted value : ",punk)

        if(punk==1):
            if((final[key]['name'] is not None) and (final[key]['latitude'] is None or final[key]['longitude'] is None) and (punk == 1)):
                final[key]['media_url'] = image_url
                print("Case 1")
                client = Client(account_sid, auth_token)
                response = emoji.emojize("""
You have successfully uploaded image of the pothole ! :white_heavy_check_mark:

NEXT

*Follow the set of steps , to be given , carefully to send your current location.* :globe_with_meridians: 

You can also choose to send your location directly , if know the process of doing it.

Else , to view the steps of sending current location , reply *Location* to view the steps.
""", use_aliases=True)
                message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

                responded = True
                # print("\n\n",final,"\n\n")
                
            

            elif((final[key]['name'] is None) and (final[key]['latitude'] is None or final[key]['longitude'] is None) and (punk == 1)):
                final[key]['media_url'] = image_url
                print("Case 2")
                client = Client(account_sid, auth_token)
                response = emoji.emojize("""
You have successfully uploaded image of the pothole ! :white_heavy_check_mark:

But you have not entered your name and sent your live location yet.

Enter your Fullname in the following format :

*My name is <YOUR-FULLNAME>* 

After entering your name in the format specified above , send your live location.

If you do not know how to send your live location using Whatsapp , reply *Location* to view the steps.
""", use_aliases=True)
                message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

                responded = True
                # print("\n\n",final,"\n\n")
            

            elif((final[key]['name'] is None) and (final[key]['latitude'] is not None or final[key]['longitude'] is not None) and (punk == 1)):
                final[key]['media_url'] = image_url
                print("Case 3")
                client = Client(account_sid, auth_token)
                response = emoji.emojize("""
You have successfully uploaded image of the pothole ! :white_heavy_check_mark:

You have successfully sent your live location as well ! :white_heavy_check_mark:

But you have not entered your name yet.

Enter your Fullname in the following format :

*My name is <YOUR-FULLNAME>* 
""", use_aliases=True)
                message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

                responded = True
                # print("\n\n",final,"\n\n")

            elif((final[key]['name'] is not None) and (final[key]['latitude'] is not None or final[key]['longitude'] is not None) and (punk == 1)):
                final[key]['media_url'] = image_url
                print("Case 4")
                client = Client(account_sid, auth_token)
                response = emoji.emojize("""
You have successfully uploaded image of the pothole ! :white_heavy_check_mark:

And with that , you have successfully registered your complaint.
""", use_aliases=True)
                message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

                responded = True
                print("\n\n",final,"\n\n")
                #store data into model here
                whatsapp = whatsapp_data()

                whatsapp.complaint_id = final[key]['image_id']
                number = get_key(final[key])
                whatsapp.number = number[9:]
                whatsapp.name = final[key]['name']
                whatsapp.save()

                current_complaint = pothole()

                current_complaint.complaint_id = str(final[key]['image_id'])
                current_complaint.uploaded_timestamp = timezone.now()
                current_complaint.coordinates = str(final[key]['latitude'])+','+str(final[key]['longitude'])
                current_complaint.address = final[key]['address']
                current_complaint.pothole_image = str(final[key]['image_id'])+'.jpg'
                current_complaint.ward_no = int(final[key]['ward_no'])
                current_complaint.origin = 'whatsapp'
                current_complaint.save()

                duplicate_check('Recent',final[key]['ward_no'])

                del final[key]
            

        elif(punk==0):
            client = Client(account_sid, auth_token)
            response = emoji.emojize("""
You have not uploaded image of the pothole ! :cross_mark:

You have to upload the image of the pothole.
""", use_aliases=True)
            message = client.messages \
                .create(
                    from_='whatsapp:+14155238886',
                    body= response,
                    to=request.POST['From']
                )

            responded = True
            # print("\n\n",final,"\n\n")



    elif incoming_msg == 'location':

        client = Client(account_sid, auth_token)

        response = emoji.emojize("""
:black_small_square: *'Step 1' :* On the chatbox , Tap Attach :paperclip: > Location 


If you have understood this step , reply *BR*.
""", use_aliases=True)
        message = client.messages \
            .create(
                from_='whatsapp:+14155238886',
                body= response,
                media_url = 'https://api.twilio.com/2010-04-01/Accounts/AC9304409e5dd28f2e399194f0f6d92b5a/Messages/MM11dea5cc736058a85ee29ec812291708/Media/MEe84be185eb89bbc25a8dbee7e3de68b8',
                to=request.POST['From']
            )

        responded = True


    elif incoming_msg == 'br':

        client = Client(account_sid, auth_token)

        response = emoji.emojize("""
:black_small_square: *'Step 2' :* If your GPS services is disabled , the message as shown in this image will be displayed.

Enable location permissions for WhatsApp in your phone's *Settings* > *Apps & notifications* > *Advanced* > *App permissions* > *Location* > turn on *WhatsApp*.


If you have understood this step , reply *CR*.
""", use_aliases=True)
        message = client.messages \
            .create(
                from_='whatsapp:+14155238886',
                body= response,
                media_url = 'https://api.twilio.com/2010-04-01/Accounts/AC9304409e5dd28f2e399194f0f6d92b5a/Messages/MMdc82dd2ed49906c5397b8fc2e7972428/Media/ME856572c7f0f1f2f5708a8a19e3888c17',
                to=request.POST['From']
            )

        responded = True


    elif incoming_msg == 'cr':

        client = Client(account_sid, auth_token)

        response = emoji.emojize("""
:black_small_square: *'Step 3' :* The Location Services interface will have a display as shown in this image.

*Be Sure that Location permission for Whatsapp is enabled*.

If you have understood this step , reply *DR*.
""", use_aliases=True)
        message = client.messages \
            .create(
                from_='whatsapp:+14155238886',
                body= response,
                media_url = 'https://api.twilio.com/2010-04-01/Accounts/AC9304409e5dd28f2e399194f0f6d92b5a/Messages/MM234b753a27f84b022d84f8b99b00daa9/Media/ME5697f307a4a9a5dd1f516970b72be535',
                to=request.POST['From']
            )

        responded = True


    elif incoming_msg == 'dr':
        
        client = Client(account_sid, auth_token)

        response = emoji.emojize("""
:black_small_square: *'Step 4' :* Now in your Whatsapp chatbox , Tap Attach :paperclip: > Location 

A interface , as shown in this image , will open.

Tap on *Send your Current Location* , and your live location will be sent.

If you have understood all the steps , send your live location , following the given instructions.
""", use_aliases=True)
        message = client.messages \
            .create(
                from_='whatsapp:+14155238886',
                body= response,
                media_url = 'https://api.twilio.com/2010-04-01/Accounts/AC9304409e5dd28f2e399194f0f6d92b5a/Messages/MMb64d80e4c04dc005536388ac92562d2e/Media/MEc53a58b4604445cb93d22df81a419f4c',
                to=request.POST['From']
            )

        responded = True


    elif 'Latitude' in request.POST.keys():
        key = str(request.POST['From'])
        if key not in final.keys():
            l.append(key)
            final[key] = dict.fromkeys(l1)
            l=[]

            
        final[key]['latitude'] = request.POST['Latitude']
        final[key]['longitude'] = request.POST['Longitude']
        str1 = str(final[key]['latitude']+','+final[key]['longitude'])
        GeoFetch(key, str1)
        latitude = Decimal(final[key]['latitude'])
        longitude = Decimal(final[key]['longitude'])
        ward = Get_Ward(latitude,longitude)
        final[key]['ward_no'] = ward
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        final[key]['created_at'] = now

        if(final[key]['name'] is not None and final[key]['media_url'] is not None):
            response = emoji.emojize("""
You have successfully sent your live location ! :white_heavy_check_mark:

And with this , you have successfully lodged your complaint.
""", use_aliases=True)
            msg.body(response)
            responded = True
            print("\n\n",final,"\n\n")
            #store data into model here
            whatsapp = whatsapp_data()
            whatsapp.complaint_id = final[key]['image_id']
            number = get_key(final[key])
            whatsapp.number = number[9:]
            whatsapp.name = final[key]['name']
            whatsapp.save()

            current_complaint = pothole()

            current_complaint.complaint_id = str(final[key]['image_id'])
            current_complaint.uploaded_timestamp = timezone.now()
            current_complaint.coordinates = str(final[key]['latitude'])+','+str(final[key]['longitude'])
            current_complaint.address = final[key]['address']
            current_complaint.pothole_image = str(final[key]['image_id'])+'.jpg'
            current_complaint.ward_no = int(final[key]['ward_no'])
            current_complaint.origin = 'whatsapp'
            current_complaint.save()

            duplicate_check('Recent',final[key]['ward_no'])

            del final[key]

        elif(final[key]['name'] is None and final[key]['media_url'] is not None):
            response = emoji.emojize("""
You have successfully sent your live location ! :white_heavy_check_mark:

You have successfully uploaded image of the pothole as well ! :white_heavy_check_mark:

But you have not entered your name yet.

Enter your Fullname in the following format :

*My name is <YOUR-FULLNAME>* 
""", use_aliases=True)
            msg.body(response)
            responded = True
            # print("\n\n",final,"\n\n")

        elif(final[key]['name'] is not None and final[key]['media_url'] is None):
            response = emoji.emojize("""
You have successfully sent your live location ! :white_heavy_check_mark:

You have successfully entered your name as well ! :white_heavy_check_mark:

But you have not uploaded an image of the pothole yet.

Upload an image of the pothole.

If you do not know how to upload an image using Whatsapp , reply *Image* to view the steps.
""", use_aliases=True)
            msg.body(response)
            responded = True
            # print("\n\n",final,"\n\n")

        else:
            response = emoji.emojize("""
You have successfully sent your live location ! :white_heavy_check_mark:

But you have not entered your name and uploaded a picture of the pothole yet.

Enter your Fullname in the following format :

*My name is <YOUR-FULLNAME>* 

After entering your name in the format specified above , upload the image of the pothole.

If you do not know how to upload an image using Whatsapp , reply *Image* to view the steps.
""", use_aliases=True)
            msg.body(response)
            responded = True
            # print("\n\n",final,"\n\n")

    
    if not responded:
        msg.body("Sorry, I don't understand. Reply *Hello* for a list of commands.")

    return (str(resp))