from __future__ import print_function


import googlemaps
import json
import os
import csv
import sys
import json
from six.moves.urllib.request import urlopen


def GoogPlac(lat,lng,radius,types,key):
  #making the url
  AUTH_KEY = key
  LOCATION = str(lat) + "," + str(lng)
  RADIUS = radius
  TYPES = types
  MyUrl = ('https://maps.googleapis.com/maps/api/place/nearbysearch/json'
           '?location=%s'
           '&radius=%s'
           '&types=%s'
           '&sensor=false&key=%s') % (LOCATION, RADIUS, TYPES, AUTH_KEY)
  #grabbing the JSON result
  DEFAULT_ENCODING = 'utf-8'
  
  urlResponse = urlopen(MyUrl)

  if hasattr(urlResponse.headers, 'get_content_charset'):
    encoding = urlResponse.headers.get_content_charset(DEFAULT_ENCODING)
  else:
    encoding = urlResponse.headers.getparam('charset') or DEFAULT_ENCODING

  output = json.loads(urlResponse.read().decode(encoding))



  return output

'''
def print_js(js1, file1):
  rootDir1 = 'c:/IEDC/Module3/Places/Utilities/'
  x_file1 = rootDir1 + '/' + file1
  with open(x_file1,'w') as data3:
    js_s=json.dumps(js1, indent=4, sort_keys=True)
    data3.write(js_s)

  s="Written"
  return s
'''

#rootDir = 'c:/Proj2/Submit/fbfeed'

def common_elements(list1, list2):
    return [element for element in list1 if element in list2]

#fname="atm_1.json"
lati= 19.1239
longi= 72.8361


pl=(GoogPlac(lati,longi,500,'department_store,store,bakery,beauty_salon,bicycle_store,book_store,car_repair,clothing_store,electronics_store,florist,furniture_store,hair_care,hardware_store,jewelry_store,laundary,pet_store,pharmacy,plumber,shoe_store,shopping_mall','AIzaSyA6udyv0riUcZQnn_8TqzqMjOevOIcZHX4'))

#print_js(pl,fname)

list1 = ['department_store','store','bakery','beauty_salon','health','bicycle_store','book_store','car_repair','clothing_store','electronics_store','florist','furniture_store','hair_care','hardware_store','jewelry_store','laundary','pet_store','pharmacy','plumber','shoe_store,shopping_mall']

# print(pl['results'][9]['types'])


# print(list(set(list1).intersection(pl['results'][19]['types'])))

'''
for i in range(len(pl['results'])):
	if len(common_elements((pl['results'][i]['types']),list1)) != 0:
		print(pl['results'][i]['name'] )
		print(common_elements((pl['results'][i]['types']),list1))

'''


