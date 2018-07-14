#!/usr/bin/env python3
import quandl
import os

def init_quandl():
    try:
        quandl.ApiConfig.api_key=os.environ['quandl_key']
    except Exception as e:
        print("set os.environ['quandl_key'] to set the api key")
        exit(1)

def get_single_data(code,date):
    try:
        k  = quandl.get(code, start_date=date, end_date=date)
    except Exception as e:
        print('something went wrong while fecthing data from quandl {0}'.format(e))
    return k

init_quandl()
print(get_single_data('AMFI/351','2018-07-09'))

