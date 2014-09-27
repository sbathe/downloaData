#!/usr/bin/python
import sqlite3
import urllib, json, datetime, time, os.path
try:
  conn = sqlite3.connect('test.db')
except:
  print "Cannot connect to or create db"
  sys.exit(2)

c = conn.cursor()
def ifTableExists(table):
  t = (table,)
  return c.execute('''select count(*) FROM sqlite_master WHERE type='table' AND name='%s' ''' % t).fetchone()[0]

def prep_db():
    print "Preparing / Seeding the db"
    try:
      c.execute('''CREATE TABLE init (init_type text, status int)''')
      c.execute('''CREATE TABLE lastupdate (timestamp text)''')
      c.execute('''CREATE TABLE mfid_name (mfid int, house_id int, name text)''')
      c.execute('''CREATE TABLE id_house (house_id int, house_name text)''')
      c.execute('''CREATE TABLE amfi_amc_codes (code int, amc text)''')
      c.executemany('''INSERT INTO amfi_amc_codes VALUES (?,?)''',tuple([ line.split(',') for line in open('amfi_amc_codes.list')]))
      conn.commit()
    except:
      print "Cannot initialize the DB"
      sys.exit(2)
    c.execute('''INSERT INTO init VALUES ('db_prep', 1)''')
    conn.commit()

def get_historical_data():
  '''Get historical data till todays date'''
  pass

def update_data():
  '''Handle the daily updates or updates from last updated time'''
  pass

if ifTableExists('init'):
  pass
else:
  prep_db()

