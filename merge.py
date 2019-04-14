#!/usr/bin/env python

from filetools import JsonReader, Writer
import sys

def merge(with_medicines, with_locations):
  if with_medicines["medicines"] and with_locations["locations"]:
    with_medicines["locations"] = with_locations["locations"]
    return with_medicines
  return None

if __name__ == '__main__':
  with_medicines_file = sys.argv[1]
  with_locations_file = sys.argv[2]
  iter_m = JsonReader(with_medicines_file).lines()
  iter_l = JsonReader(with_locations_file).lines()
  writer = Writer(sys.argv[3])
  try:
    while True:
      with_medicines = iter_m.next()
      with_locations = iter_l.next()
      merged = merge(with_medicines, with_locations)
      if merged:
        writer.write_json(merged)
  except StopIteration:
    pass
