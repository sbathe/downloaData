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
               meta['scheme_code'] = scheme_code
               collname = 'c'+scheme_code
               ### get a new method
               if not collname in self.DB.list_collection_names():
                 coll = self.DB.create_collection(collname)
               else:
                 coll = self.DB.get_collection(collname)
               ### end get a new method
               coll.update_one({"scheme_code": scheme_code},{"$set": {"meta": meta}}, True)
               # data is not getting inserted at all
               for year in data[amc_name][scheme_code]['data'].keys():
                   key = 'year{0}'.format(year)
                   coll.update_one({"scheme_code": scheme_code},{"$set":{key: data[amc_name][scheme_code]['data'][year]}},True)
