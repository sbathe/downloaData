#!/usr/bin/python
# -*- coding: utf_8 -*-

import sqlite3, logging,re
import urllib, json, time, os, sys

# Setup logging
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.INFO)
# Console logging, should disable once we get to automated runs
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

try:
  conn = sqlite3.connect('test.db')
  conn.text_factory = sqlite3.OptimizedUnicode
except:
  logger.error("Cannot connect to or create db")
  sys.exit(2)

c = conn.cursor()
def ifTableExists(table):
  t = (table,)
  return conn.execute('''select count(*) FROM sqlite_master WHERE type='table' AND name='{0}' '''.format(table)).fetchall()

def execute(cursor, *text):
  try:
    cursor.execute(*text)
  except:
    e = sys.exc_info()[0]
    logger.error("Cannot execute statement {0}. The error was: {1}".format(text, e))

def prep_db():
    logger.info("Preparing / Seeding the db")
    execute(c,'''CREATE TABLE init (init_type text, status int, lastupdate text)''')
    execute(c,'''CREATE TABLE lastupdate (mfid int, date text)''')
    execute(c,'''CREATE TABLE mfid_name_map (mfid int, house_id int, name text)''')
    execute(c,'''CREATE TABLE amfi_amc_codes (code int, amc text)''')
    conn.executemany('''INSERT INTO amfi_amc_codes VALUES (?,?)''', tuple([ line.split(',') for line in open('amfi_amc_codes.list')]))
    execute(c,'''INSERT INTO init VALUES ('db_prep', 1, time.time())''')
    conn.commit()

def get_data_from_amfi(url,house_id):
  """This retuns data as a list of semi-colon delimited srtings, in format:
     Scheme Code;Scheme Name;Net Asset Value;Repurchase Price;Sale Price;Date\r\n
     We are only interested on code, name, nav and date"""
  try:
      uconn = urllib.urlopen(url)
  except IOError:
      time.sleep(300)
  except:
      logger.error("Cannot fetch data from AMFI site for {0}".format(url))
  if uconn.code == 200:
    data = uconn.readlines()
    uconn.close()
    fname = 'rawdata/' + str(house_id)
    try:
      os.stat(os.path.dirname(fname))
    except:
      os.makedirs(os.path.dirname(fname))
    fh = open(fname,'w')
    for l in data:
      print>>fh,l
    fh.close()
  else:
    logger.error("Cannot fetch data from AMFI site for %s , code %d" % name, code)
  return data

def get_historical_data(start_date = '01-Jan-2010'):
  '''Get historical data till todays date'''
  end_date = time.strftime('%d-%b-%Y',time.localtime())
  histdata_base_url = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&frmdt=%s&todt=%s&mf=' % (start_date, end_date)
  amc_codes = c.execute('''SELECT * from amfi_amc_codes''').fetchall()
  for t in amc_codes:
    mfid_name_map = conn.execute('''SELECT * FROM mfid_name_map''').fetchall()
    house_id, name = t
    url = histdata_base_url + str(house_id)
    logger.info('getting data from %s' % url)
    try:
      data = open('rawdata/'+str(house_id)).readlines()
    except:
      data = get_data_from_amfi(url,house_id)
    for line in data:
      mf_id=line.split(';')[0]
      if re.match(r'\d',mf_id):
        mf_id,mf_name,mf_nav,g1,g2,date=line.split(';')
        t = (str(mf_id), house_id, mf_name)
        if t in mfid_name_map:
          pass
        else:
          mfid_name_map.append(t)
        # Check if we already have this record
        if ifTableExists(mf_id):
          get_last_update = conn.execute('''SELECT date from lastupdate where mfid = {0}'''.format(mf_id)).fetchall()
          last_update_date = get_last_update[0][0] if get_last_update else '01-Jan-2010'
          logger.debug('comparing last_update_date, {0} with date from data, {1}'.format(last_update_date,date))
          if time.mktime(time.strptime(last_update_date,'%d-%b-%Y')) < time.mktime(time.strptime(date.strip(),'%d-%b-%Y')):
            try:
              conn.execute('''INSERT INTO '{0}' VALUES (?,?)'''.format(mf_id), (date.strip(), mf_nav))
            except:
              e = sys.exc_info()[0]
              logger.error('Failed to update table {0} for date {1}. The error is {2}'.format(mf_id,date.strip(),e))
            if get_last_update:
                conn.execute('''UPDATE lastupdate set date = '{0}' where mfid = {1}'''.format(date.strip(), mf_id))
            else:
                conn.execute('''INSERT INTO lastupdate VALUES (?,?)''', (mf_id,date.strip()))
        else:
          execute(c,'''CREATE TABLE '{0}' (date text, nav real)'''.format(mf_id.strip()))
          execute(c,'''INSERT INTO mfid_name_map VALUES (?,?,?)''', t)
          execute(c,'''INSERT INTO '{0}' VALUES (?,?)'''.format(mf_id), (date.strip(), mf_nav))
  os.remove('rawdata/'+str(house_id))
  execute(c,'''UPDATE lastupdate SET date = '{0}' where mfid = 'all' '''.format(end_date))

'''
  def update_data():
  Handle the daily updates or updates from last updated time
  1. Get last update date
     2. Get historical data from last_update_date till today
  lastupdate = conn.execute("SELECT date from lastupdate where mfid = 'all' ").fetchall()
  get_historical_data(start_date = lastupdate )
'''
  
if __name__ == "__main__":
  if ifTableExists('init'):
    pass
  else:
    prep_db()
  lastupdate = conn.execute('''SELECT date from lastupdate where mfid = 'all' ''').fetchall()
  if lastupdate:
    lpd = lastupdate[0][0]
    logger.info('Downloading data from date {0}'.format(lpd))
    get_historical_data(start_date = lpd )
  else:
    logger.info('Downloading data from date 01-Jan-2010')
    get_historical_data()
