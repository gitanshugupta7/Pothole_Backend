import tweepy
import json
import csv
from random import randint
import uuid
import json
import wget
import urllib
import urllib3
import requests
import shutil
from random import randint
import sys, time
import random
from django.utils import timezone
from shapely.geometry import Point, shape
# import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','project.settings')
import django
django.setup()
from duplicator import duplicate_check

import potholedetector
from geopy.geocoders import GoogleV3

from app1.models import twitter_data, pothole

auth = tweepy.OAuthHandler('s85wrlCQW61WWdL9TvPWXQgw5', 'bZ7vPutHBH1qqvI4VEfJYmK51WVUlJRoCLJnLtvkUMknxriJbx')
auth.set_access_token('1208629520451850245-YvBQWMfQYzBROSwSHDeW3fWd4Gc5rz',
                      'GFqVTnqSzEQ5KeS6EzswMkcl3avAfWOHSNY0QtdiuW163')

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

flag = 1
count = 1
status = "Tweet was successful"
unique_id = ''

print("twitter running")

class tweetparse7:

    def __init__(self):
        self.str1 = ""
        self.final = dict()

    def GeoFetch(self, point):
        geocoder = GoogleV3(api_key='AIzaSyDJrBe_VguWvYK8pZhEjKd3sxituvoK2hI')
        address = geocoder.reverse(point)
        self.final['address'] = address

    def Get_Ward(self,my_lat,my_long):
        with open('C:/Users/GITANSHU/DjangoAPI/Pothole_Backend_Kolkata/kolkata.geojson') as f:
            js = json.load(f)

        point = Point(my_long,my_lat)

        for feature in js['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return feature['properties']['WARD']

    def Convert(self, lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

    def Parsing(self, test_dict):
        global count
        global flag
        global status
        global local_image
        global unique_id
        flag = 1
        status = "Tweet was successful"
        auth = tweepy.OAuthHandler('s85wrlCQW61WWdL9TvPWXQgw5', 'bZ7vPutHBH1qqvI4VEfJYmK51WVUlJRoCLJnLtvkUMknxriJbx')
        auth.set_access_token('1208629520451850245-YvBQWMfQYzBROSwSHDeW3fWd4Gc5rz',
                              'GFqVTnqSzEQ5KeS6EzswMkcl3avAfWOHSNY0QtdiuW163')
        api = tweepy.API(auth)

        d = json.loads(test_dict)
        for j in d:

            if (j == 'created_at'):
                self.final['created_at'] = d[j]
            if (j == 'user'):
                self.final['tweet_id'] = str(d['id'])
                self.final['name'] = d[j]['name']
                self.final['username'] = d[j]['screen_name']

            if (j == 'place'):

                if (d[j] is None):
                    i7 = '@' + d['user']['screen_name']
                    m1 = i7 + " " + "Dear User , you have not shared your live location , Tweet Failed"
                    try:
                        api.update_status(m1 , d['id'])
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            print("An error occured")
                        else:
                            raise error
                    del d[j]
                    flag = 0
                    status = "User did not share his location , Tweet failed"
                    self.final = {}
                    break

                else:
                    if (d[j]['bounding_box'] != 'null'):
                        latitude = d[j]['bounding_box']['coordinates'][0][0][1] 
                        longitude = d[j]['bounding_box']['coordinates'][0][0][0] 
                        self.str1 = str(latitude) + ',' + str(longitude)
                        ward = self.Get_Ward(latitude,longitude)
                        self.final['ward_no'] = ward
                        self.final['coordinates'] = self.str1
                        self.GeoFetch(self.str1)

            if (j == 'entities'):
                if('media' in d[j]):
                    image_url = d[j]['media'][0]['media_url']
                    self.final['image url'] = image_url
                    resp = requests.get(image_url, stream=True)
                    unique_id = str(uuid.uuid4())
                    local_file = open('C:/Users/GITANSHU/DjangoAPI/Pothole_Backend_Kolkata/media/' + unique_id + '.png', 'wb')
                    local_image = unique_id + '.png'
                    resp.raw.decode_content = True
                    shutil.copyfileobj(resp.raw, local_file)
                    p = potholedetector.Image(unique_id)
                    if p==1 :
                        print("Gadda hain bhai")
                    else:
                        print("Gadda nai hain bhai jhut bol raha hain")
                        self.final = {}
                        #os.remove('C:/Users/GITANSHU/DjangoAPI/project/media/'+unique_id+'.jpg')
                        i7 = '@' + d['user']['screen_name']
                        m1 = i7 + " " + "Dear User , you have not posted photo of the pothole, please upload a valid image, Tweet Failed"
                        try:
                            api.update_status(m1, d['id'])
                        except tweepy.TweepError as error:
                            if error.api_code == 187:
                                print("An error occured")
                            else:
                                raise error
                        del d[j]
                        flag = 0
                        break
                    del resp
                else:
                    i7 = '@' + d['user']['screen_name']
                    m1 = i7 + " " + "Dear User , you have not posted photo of the pothole , Tweet Failed"
                    try:
                        api.update_status(m1, d['id'])
                    except tweepy.TweepError as error:
                        if error.api_code == 187:
                            print("An error occured")
                        else:
                            raise error
                    del d[j]
                    flag = 0
                    status = "User did not upload picture of the pothole , Tweet failed"
                    self.final = {}
                    break


        if(flag == 1):
            i7 = '@' + d['user']['screen_name']
            m = i7 + " " + "Complaint no :" + str(
                count) + "--" + " Your complaint has been successfully received , Congrats ."
            count += 1
            try:
                api.update_status(m, d['id'])
            except:
                print()


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API

        listener = StdOutListener(fetched_tweets_filename)

        auth = tweepy.OAuthHandler('s85wrlCQW61WWdL9TvPWXQgw5', 'bZ7vPutHBH1qqvI4VEfJYmK51WVUlJRoCLJnLtvkUMknxriJbx')
        auth.set_access_token('1208629520451850245-YvBQWMfQYzBROSwSHDeW3fWd4Gc5rz',
                              'GFqVTnqSzEQ5KeS6EzswMkcl3avAfWOHSNY0QtdiuW163')

        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords:
        stream.filter(track=hash_tag_list)
        stream.send_direct_message("Your complaint has been received", "Thank You For Reporting")


"""

# # # # TWITTER STREAM LISTENER # # # #

"""


class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):

        global flag
        try:

            with open(self.fetched_tweets_filename, 'a') as tf:
                print(data)
                tp = tweetparse7()
                tp.Parsing(data)
                res = not tp.final
                if(res is True):
                    print("No data to store")
                else:
                    current_complaint = pothole()
                    current_tweet = twitter_data()

                    current_tweet.complaint_id = unique_id
                    current_tweet.tweet_id = tp.final['tweet_id']
                    current_tweet.name = tp.final['name']
                    current_tweet.username = tp.final['username']
                    current_tweet.save()

                    current_complaint.complaint_id = unique_id
                    current_complaint.uploaded_timestamp = timezone.now()
                    current_complaint.coordinates = tp.final['coordinates']
                    current_complaint.address = tp.final['address']
                    current_complaint.pothole_image = local_image
                    current_complaint.ward_no = tp.final['ward_no']
                    current_complaint.origin = 'twitter'
                    current_complaint.save()

                    duplicate_check('Recent',tp.final['ward_no'])
           
            return True

        except BaseException as e:
            print("Error on_data %s" % str(e))
            return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["KMCPothole"]
    fetched_tweets_filename = "tweets_without_ML.txt"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)