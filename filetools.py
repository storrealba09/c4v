from yaml.reader import Reader as YamlReader

import io
import yaml
import json

def strip_invalid(s):
    res = ''
    for x in s:
        if YamlReader.NON_PRINTABLE.match(x):
            # res += '\\x{:x}'.format(ord(x))
            continue
        res += x
    return res

class State(object):

  def __init__(self):
    self.dropped = 0
    self.processed = 0

  def inc(self):
    self.processed = self.processed + 1

  def dec(self):
    self.dropped = self.dropped + 1

class Reader(object):

  def __init__(self, file):
    self.__file = file
    self.__state = State()

  def process(self, line):
    return line

  def lines(self):
    with io.open(self.__file, 'r', encoding='utf-8') as input:
      for line in input:
        try:
          tweet = self.process(line)
          self.__state.inc()
          yield tweet
        except: 
          self.__state.dec()

  def state(self):
    return self.__state

  def processed(self):
    return self.__state.processed

  def dropped(self):
    return self.__state.dropped

class JsonReader(Reader):

  def process(self, line):
    return yaml.load(strip_invalid(line))

class CsvReader(Reader):

  def process(self, line):
    return strip_invalid(line).split(',')

class Writer(object):

  def __init__(self, file):
    self.__handle = io.open(file, 'w', encoding='utf-8')

  def write(self, s):
    self.__handle.write(self.line(s))

  def write_json(self, js):
    self.write(json.dumps(js))

  @staticmethod
  def line(s):
    return unicode(s.replace('\n', ' ').replace('\r', ' ') + '\n')
