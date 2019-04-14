#!/usr/bin/env python

from filetools import CsvReader, JsonReader, Writer
import re
import sys

class Medicines(object):
    def __init__(self,file):
        self.medicines = {}
        for line in CsvReader(file).lines():
            self.new_medicine(str(line[0]).strip())

    def new_medicine(self,entry):
        parts = re.compile(r'\s*\+\s*').split(entry)
        parts = [p.replace('*','') for p in parts]
        for p in parts:
            self.medicines[p] = entry

    def match(self, word, matcher = None):
        _matcher = matcher if matcher else self.DelfaultMatcher(self.medicines.keys())
        matched_key = _matcher.match(word)
        return self.medicines[matched_key] if matched_key else None

    class DelfaultMatcher(object):
        def __init__(self,keys):
            self.keys = keys

        def match(self, word):
            for key in self.keys:
                if word.upper() == key:
                    return key
            return None

class Medicine(object):

  def __init__(self, record, medicines):
    self.__record = record
    self.medicines = medicines
    self.__resolve()

  def get(self):
   return self.__record

  def __resolve(self):
    if 'entities' not in self.__record:
      return None
    self.__record['medicines'] = list(filter(lambda x: x is not None, map(self.medicines.match, self.__record['entities'])))


if __name__ == '__main__':
  reader = JsonReader(sys.argv[1])
  writer = Writer(sys.argv[2])
  medicines = Medicines('WHO_Medicine_List.csv')
  for line in reader.lines():
    writer.write_json(Medicine(line, medicines).get())
  print 'Processed: {}'.format(reader.processed())
  print 'Dropped: {}'.format(reader.dropped())
