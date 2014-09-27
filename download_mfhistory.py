#!/usr/bin/python
import urllib, json, time, os.path
error = ''
base_amfi_url = 'http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?tp=1&frmdt=01-Jan-2010&todt=10-Jun-2014&mf='
#base_url = 'https://ichart.finance.yahoo.com/table.csv?s='
log_error = []
for l in open('error_log').readlines():
  log_error.append(l.split(':')[0])

error_log = open('error_log','w')
for l in open('amfi_amc_codes.list').readlines():
  code = l.split(',')[0]
  name = l.split(',')[1].strip()
  url = base_amfi_url + code
  file_name = name.replace(' ','_') + '.csv'
  if code in log_error:
    print 'data not available for %s' % code
    continue
  if os.path.isfile(file_name):
    print 'file %s exists, not downloading again' % file_name
    continue
  time.sleep(15)
  try:
    t = urllib.urlopen(url)
  except IOError:
    # wait 5 minutes for the n/w connection
    time.sleep(300)
  if t.code == 200:
    print 'writing data for %s to csv' % (name)
    file_name = name.replace(' ','_').replace('/','_') + '.csv'
    fh = open(file_name,'w')
    open(file_name,'w').write(t.read())
  else:
    error_log.write(code)
