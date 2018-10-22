#!/usr/bin/env python3
import requests, bs4
import json, os
import time

class amfi:
    def __init__(self):
        self.CODES_URL = 'https://www.amfiindia.com/nav-history-download'
        self.NAV_URL_TEMPLATE = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&'
        self.START_DATE = '01-Apr-2008'
        self.END_DATE = time.strftime('%d-%b-%Y',time.localtime())

    def get_url_data(self,url):
        try:
            r = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            return None
        return r.text

    def get_amc_codes(self):
        url = 'https://www.amfiindia.com/nav-history-download'
        r = self.get_url_data(url)
        if r:
          soup = bs4.BeautifulSoup(r, 'html.parser')
          NavDownMFName =  soup.find_all("select",id="NavDownMFName")
          amc_codes = { e.string:e.attrs['value'] for e in NavDownMFName[0].findAll('option') if e.attrs['value'] != ''}
        else:
           amc_codes = None
        return amc_codes

    def write_file(self,fh,data):
        #Add some validations here
        try:
            fh.write(data)
            fh.close()
        except:
            print("Unexpected error:{0}".format(sys.exc_info()[0]))

    def get_amc_nav_data(self,amc,start_date=None,end_date=None):
        if start_date is None:
            start_date = self.START_DATE
        if end_date is None:
            end_date = self.END_DATE
        url = self.NAV_URL_TEMPLATE + 'frmdt=' + start_date + '&todt=' + end_date + '&mf=' + amc
        data = self.get_url_data(url)
        return data

    def write_amc_files(self):
        amc_pairs = self.get_amc_codes()
        for amc_name, amc_code in amc_pairs.items():
            data = self.get_amc_nav_data(amc_code,start_date=self.START_DATE,end_date=self.END_DATE)
            filename = '_'.join(amc_name.split()) + '.csv'
            self.write_file(open(os.path.join('amfidata',filename),'a+'), data)
            time.sleep(120)
