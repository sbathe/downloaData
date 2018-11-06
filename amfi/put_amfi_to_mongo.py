#!/usr/bin/env python3
from amfi import AmfiDownload
from amfi import AmfiParse
import pymongo

class AmfiMongo:
    def __init__(self):
        # pull config data here
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        self.DB = client.amfi

    def write_jsons_to_docments(self, in_dir):
       amfidownloadobj = AmfiDownload()
       amfiparseobj = AmfiParse()
       amc_pairs = amfidownloadobj.get_amc_codes()
       for amc_name, amc_code in amc_pairs.items():
           data = amfiparseobj.get_json_from_amc_csvs(amc_name,in_dir)
           if not data:
               continue
           for scheme_code in data[amc_name].keys():
               meta = data[amc_name][scheme_code]['meta']
               collname = 'c'+scheme_code
               ### get a new method
               if not collname in self.DB.list_collection_names():
                 coll = self.DB.create_collection(collname)
               else:
                 coll = self.DB.get_collection(collname)
               coll.create_index(['scheme_code','year', 'scheme_name'])
               ### end get a new method
               #coll.update_one({"scheme_code": scheme_code},{"$set": {"meta": meta}}, True)
               for yearstr in data[amc_name][scheme_code]['data'].keys():
                   ydata = data[amc_name][scheme_code]['data'][yearstr]
                   ydata['scheme_code'] = scheme_code
                   try:
                       coll.insert_many([meta, ydata],ordered=False)
                   except pymongo.errors.BulkWriteError:
                       pass
