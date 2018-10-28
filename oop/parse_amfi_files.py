#!/usr/bin/env python3
import requests, bs4
import json, os
import time, datetime
import re

class AmfiParse:
   def __init__(self):
        self.NODATA = re.compile('No data found on the basis of selected parameters for this report')
        self.HEADING = re.compile('Scheme Code;Scheme Name')
        self.OPENENDED = re.compile('Open Ended Scheme')
        self.AMC = re.compile('Mutual Fund')

   def nodata(self,raw_string):
       """ Checks if the data file has any useful info """
       if re.search(self.NODATA,raw_string):
           return True
       else:
           return False

   def process_raw(self,raw_string):
       """ This will remove all blank lines from the downloaded file. Returns
       a list of non-blank lines"""
       return [ line for line in raw_string.split('\n') if line.strip() ]
   def parse(self,processed_data):
       """ The goal is:
           - Create a scheme code wise json structure with 2 sections:
           - meta: a dictionary that has scheme name, fund AMC, category etc
           - data: list of (date, NAV) tuples
       """
       data = {}
       for line in processed_data:
           if re.search(self.HEADING,line):
               headings = line.split(';')
           elif re.search(self.OPENENDED,line):
              c = []
              parts = line.split('(')
              for p in parts:
                  c.append(p.split('-'))
                  categories = [item.strip(')').strip() for sublist in c for item in sublist]
           elif re.search(self.AMC,line):
              amc = line
              data[amc] = {}
           elif len(line.split(';')) > 1:
               code,name,nav,rp,sp,date = line.split(';')
               if code not in data[amc].keys():
                 data[amc][code] = {}
                 data[amc][code]["data"] = []
                 data[amc][code]["meta"] = { "name": name, "type": "open ended", "categories": categories }
               data[amc][code]["data"].append([date,nav])
       return data
