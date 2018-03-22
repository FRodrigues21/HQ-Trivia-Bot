#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import pprint
import re
from googleapiclient.discovery import build
import pytesseract as ocr
from PIL import Image

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def main():
  # Build a service object for interacting with the API. Visit
  # the Google APIs Console <http://code.google.com/apis/console>
  # to get an API key for your own application.
  service = build("customsearch", "v1",
            developerKey="AIzaSyBv9pNO3uuk-60EUmskHirnTLMzxP4P6js")

  full = ocr.image_to_string(Image.open('/Users/franciscorodrigues/Desktop/screenshot.png'))
  question = full[:full.find("?")].replace("\n", " ")
  print question
  anwsers = full[(full.find("?")+1):].split("\n")
  anwsers = filter(None, anwsers)
  print anwsers
  _question = '"'+question+'"'+ ' ('+ anwsers[0] +' | ' +anwsers[1]+ ' | ' +anwsers[2]+')'
  print _question
  res = service.cse().list(
      q=_question,
      cx='017338427531447168454:lxlmkkpmtkc',
    ).execute()
  o = [0,0,0]
  if int(res["searchInformation"]["totalResults"]) > 0:
    for item in res["items"]:
      url = item["link"]
      f = urllib.urlopen(url)
      html = f.read()
      for i in range(0,3):
        count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(full[i+1]), html))
        o[i] += count
        print o[i]
      print "---- NEXT ---"
  else:
    print "--- NO RESULTS ----"

if __name__ == '__main__':
  main()
