#!/usr/bin/env python

from filetools import JsonReader, Writer

import requests
import yaml
import sys
import urllib

class Location(object):

  def __init__(self, record):
    self.__record = record
    self.__resolve()

  def get(self):
   return self.__record

  @staticmethod
  def __extract_place(place_list):
    return place_list[0][u'geometry'][u'location']

  def __query(self, candidate):
    API_KEY = 'AIzaSyANRCfCQECUBEFYGOgPhgGNj7EsXXqc6jM'
    URL = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?inputtype=textquery&fields=geometry'
    params = '&input={q}'.format(q=urllib.quote(candidate.encode('utf-8')))
    query = '{url}{params}&key={key}'.format(url=URL, params=params, key=API_KEY)
    response = requests.get(query).json()
    print response
    if response[u'status'] == u'ZERO_RESULTS':
      return None
    return self.__extract_place(response[u'candidates'])

  def __resolve(self):
    if 'entities' not in self.__record:
      return None
    self.__record['locations'] = list(filter(lambda x: x is not None, map(self.__query, self.__record['entities'])))

if __name__ == '__main__':
  reader = JsonReader(sys.argv[1])
  writer = Writer(sys.argv[2])
  for line in reader.lines():
    writer.write_json(Location(line).get())
  print 'Processed: {}'.format(reader.processed())
  print 'Dropped: {}'.format(reader.dropped())
    
