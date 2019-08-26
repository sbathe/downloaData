#!/usr/bin/env python3
import os
import amfi

# Download data
do = amfi.AmfiDownload()
do.download_data()

# Parse and write jsons
k = amfi.AmfiParse()
k.write_json_from_csvs('/downloaData/amfidata/','/downloaData/json_data')

# move data to mongo
m = amfi.AmfiMongo()
m.write_jsons_to_docments('amfidata')

# cleanup old csvs, we do not need to keep them around
for f in [ f for f in os.listdir('/downloaData/amfidata/') if f.endswith(".csv") ]:
    os.remove(os.path.join('/downloaData/amfidata/', f))
