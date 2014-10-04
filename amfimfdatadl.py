#!/usr/bin/python
import sqlite3, logging
import urllib, json, time, os.path

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

def prep_db():
    logger.info("Preparing / Seeding the db")
    try:
      c.execute('''CREATE TABLE init (init_type text, status int, lastupdate text)''')
      c.execute('''CREATE TABLE lastupdate (timestamp text)''')
      c.execute('''CREATE TABLE mfid_name (mfid int, house_id int, name text)''')
      c.execute('''CREATE TABLE id_house (house_id int, house_name text)''')
      c.execute('''CREATE TABLE amfi_amc_codes (code int, amc text)''')
      c.executemany('''INSERT INTO amfi_amc_codes VALUES (?,?)''',tuple([ line.split(',') for line in open('amfi_amc_codes.list')]))
      c.execute('''INSERT INTO init VALUES ('db_prep', 1, time.time())''')
      conn.commit()
    except:
      logger.error("Cannot initialize the DB")
      sys.exit(2)

def get_historical_data():
  '''Get historical data till todays date'''
  histdata_base_url = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&frmdt=01-Jan-2010&todt=10-Jun-2014&mf='
  
  pass

def update_data():
  '''Handle the daily updates or updates from last updated time'''
  pass

if ifTableExists('init'):
  pass
else:
  prep_db()

