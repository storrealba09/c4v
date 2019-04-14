#!/usr/bin/env python

import yaml
import json
import sys
import io
from yaml.reader import Reader

class State(object):

  def __init__(self):
    self.dropped = 0
    self.processed = 0

def strip_invalid(s):
    res = ''
    for x in s:
        if Reader.NON_PRINTABLE.match(x):
            # res += '\\x{:x}'.format(ord(x))
            continue
        res += x
    return res

def tweet_gen(file, state):
  with io.open(file, 'r', encoding='utf-8') as input:
    for line in input:
      try:
        tweet = yaml.load(strip_invalid(line))
        state.processed = state.processed + 1
        yield tweet
      except:
        state.dropped = state.dropped + 1

def process(column, value):
  if column == 'hash_tags' and isinstance(value, list):
    return ';'.join(value)
  elif column == 'tweet_text' and value.startswith('RT'):
    raise ValueError()
  return value

def line(s):
  return unicode(s.replace('\n', ' ').replace('\r', ' ') + '\n')

if __name__ == '__main__':
  file = sys.argv[1]
  state = State()
  columns = []
  with io.open('filtered_tweets.csv', 'w', encoding='utf-8') as output:
    try:
      for tweet in tweet_gen(file, state):
        try:
          if not columns:
            columns = tweet.keys()
            output.write(line(','.join(columns)))
          values = []
          for column in columns:
            try:
              values.append(process(column, tweet[column]))
            except KeyError:
              values.append('')
          output.write(line('|'.join(values)))
        except:
          state.processed = state.processed - 1
          state.dropped = state.dropped + 1
    except KeyboardInterrupt:
      pass
  print ''
  print 'Processed: {}'.format(state.processed)
  print 'Dropped: {}'.format(state.dropped)
