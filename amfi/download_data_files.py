#!/usr/bin/env python3
import requests, bs4
import json, os, sys
import time, datetime
import logging
#from amfi import AmfiMongo
logger = logging.getLogger(__name__)
class AmfiDownload:
    def __init__(self):
        self.CODES_URL = 'https://www.amfiindia.com/nav-history-download'
        self.NAV_URL_TEMPLATE = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&'
        self.START_DATE = '01-Apr-2008'
        self.END_DATE = datetime.datetime.strftime(datetime.datetime.today(),'%d-%b-%Y')

    def get_url_data(self,url):
        try:
            r = requests.get(url,timeout=15)
        except requests.exceptions.RequestException as e:
            logger.debug('Cannot complete request to {0}. The error was:'.format(url))
            logger.debug(e)
            return None
        return r.text

    def get_amc_codes(self):
        url = self.CODES_URL
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
            logger.debug("Unexpected error:{0}".format(sys.exc_info()[0]))

    def get_amc_nav_data(self,amc,start_date=None,end_date=None):
        if start_date is None:
            start_date = self.START_DATE
        if end_date is None:
            end_date = self.END_DATE
        url = self.NAV_URL_TEMPLATE + 'frmdt=' + start_date + '&todt=' + end_date + '&mf=' + amc
        logger.debug("calling URL: {0}".format(url))
        data = self.get_url_data(url)
        return data

    def write_amc_files(self,start_date=None,end_date=None):
        if start_date is None:
            start_date = self.START_DATE
        if end_date is None:
            end_date = self.END_DATE
        amc_pairs = self.get_amc_codes()
        lockdata = {}
        today = datetime.datetime.strftime(datetime.datetime.strptime(end_date, '%d-%b-%Y'), '%s')
        for amc_name, amc_code in amc_pairs.items():
            logger.info("Getting data for amc_code: {0}".format(amc_code))
            data = self.get_amc_nav_data(amc_code,start_date=start_date,end_date=end_date)
            name = '_'.join(amc_name.split())
            filename = '_'.join([name, today]) + '.csv'
            try:
                outf = open(os.path.join('/downloaData/amfidata',filename),'w+')
            except Exception as e:
                logger.error("Cannot create file: {0}".format(e))
            self.write_file(outf, data)
            lockdata[amc_name] = end_date
            time.sleep(20)
        lockdata['global'] = end_date
        self.write_file(open('/downloaData/amfidata/lockfile.json','w+'), json.dumps(lockdata,sort_keys=True, indent=4))
        # also write this data to mongo
        #m = AmfiMongo()
        #m.write_last_updated(lockdata)


    def init_or_update(self):
        """ Returns startdate to get the data from, depending on when the
        update was perfomed last"""
        if os.path.isfile('/downloaData/amfidata/lockfile.json'):
            d = json.load(open('/downloaData/amfidata/lockfile.json'))
            s_date = datetime.datetime.strftime(datetime.datetime.strptime(d['global'],'%d-%b-%Y') + datetime.timedelta(days=1), '%d-%b-%Y')
        else:
            #m = AmfiMongo()
            #try:
            #    r = m.get_last_updated('global')
            #   s_date = datetime.datetime.strftime(datetime.datetime.strptime(r['date'],'%d-%b-%Y') + datetime.timedelta(days=1), '%d-%b-%Y')
            #except:
            #    s_date = self.START_DATE
            s_date = self.START_DATE
        return s_date

    def download_data(self):
        start_date = self.init_or_update()
        today = datetime.datetime.today()
        if datetime.datetime.strptime(start_date,'%d-%b-%Y').weekday() >= 5:
            if (today - datetime.datetime.strptime(start_date,'%d-%b-%Y')).days <= 1:
                logger.info('No need to get data, already updated locally')
                sys.exit(0)
        elif (today - datetime.datetime.strptime(start_date,'%d-%b-%Y')).days == 0:
                logger.info('No need to get data, already updated locally')
                sys.exit(0)
        self.write_amc_files(start_date=start_date)
