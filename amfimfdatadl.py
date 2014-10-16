#!/usr/bin/python
import sqlite3, logging
import urllib, json, time, os.path, sys

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
except:
  logger.error("Cannot connect to or create db")
  sys.exit(2)

c = conn.cursor()
def ifTableExists(table):
  t = (table,)
  return c.execute('''select count(*) FROM sqlite_master WHERE type='table' AND name='%s' ''' % t).fetchone()[0]

def execute(cursor, text):
  try:
    cursor.execute(text)
  except:
    logger.error("Cannot execute statement %s" % text)

def prep_db():
    logger.info("Preparing / Seeding the db")
    execute(c,'''CREATE TABLE init (init_type text, status int, lastupdate text)''')
    execute(c,'''CREATE TABLE lastupdate (timestamp text)''')
    execute(c,'''CREATE TABLE mfid_name_map (mfid int, house_id int, name text)''')
    execute(c,'''CREATE TABLE amfi_amc_codes (code int, amc text)''')
    c.executemany('''INSERT INTO amfi_amc_codes VALUES (?,?)''', tuple([ line.split(',') for line in open('amfi_amc_codes.list')]))
    execute(c,'''INSERT INTO init VALUES ('db_prep', 1, time.time())''')
    conn.commit()

def get_data_from_amfi(url):
  """This retuns data as a list of semi-colon delimited srtings, in format:
     Scheme Code;Scheme Name;Net Asset Value;Repurchase Price;Sale Price;Date\r\n
     We are only interested on code, name, nav and date"""
  try:
      uconn = urllib.urlopen(url)
  except IOError:
      time.sleep(300)
  except:
      logger.error("Cannot fetch data from AMFI site for %s , code %d" % name, code)
  if uconn.code == 200:
    data = uconn.readlines()
    uconn.close()
  else:
    logger.error("Cannot fetch data from AMFI site for %s , code %d" % name, code)
  return data

def get_historical_data():
  '''Get historical data till todays date'''
  histdata_base_url = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&frmdt=01-Jan-2010&todt=10-Jun-2014&mf='
  amc_codes = c.execute('''SELECT * from amfi_amc_codes''').fetchall()
  for t in amc_codes:
    mfid_name_map = []
    house_id, name = t
    url = histdata_base_url + house_id
    data = get_data_from_amfi(url)
    for line in data:
      mf_id,mf_name,mf_nav,g1,g2,date=line.split(';')
      if re.match(r'\d',mf_id):
        t = (mf_id, house_id, mf_name)
        if t in mfid_name_map:
          pass
        else:
          mfid_name_map.append(t)
        if ifTableExists(mf_code):
          c.execute('''INSERT INTO '%s' VALUES (?,?)''' % str(mf_id), (date, mf_nav))
        else:
          c.execute('''CREATE TABLE '%s' (date text, nav real)''' % str(mf_id))
          c.execute('''INSERT INTO '%s' VALUES (?,?)''' % str(mf_id), (date, mf_nav))
          conn.commit()

def update_data():
  '''Handle the daily updates or updates from last updated time'''
  pass

if ifTableExists('init'):
  pass
else:
  prep_db()

