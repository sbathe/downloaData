#!/usr/bin/env python3
import amfi

# Download data
do = amfi.AmfiDownload()
do.download_data()

# Parse and write jsons
k = amfi.AmfiParse()
k.write_json_from_csvs('/home/sb/repos/downloaData/amfidata/','/home/sb/repos/downloaData/json_data')

# move data to mongo
m = amfi.AmfiMongo()
m.write_jsons_to_docments('amfidata')
