#!/usr/bin/env python3
from amfi import AmfiDownload
from amfi import AmfiParse
import pymongo, datetime

class AmfiMongo:
    def __init__(self):
        # pull config data here
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        self.DB = client.amfi
        if not 'meta' in self.DB.list_collection_names():
            self.mcoll = self.DB.create_collection('meta')
            self.mcoll.create_index([('scheme_code',pymongo.ASCENDING)],unique=True)
            self.mcoll.create_index([('name', pymongo.TEXT), ('amc',pymongo.TEXT)])

    def write_jsons_to_docments(self, in_dir):
       amfidownloadobj = AmfiDownload()
       amfiparseobj = AmfiParse()
       amc_pairs = amfidownloadobj.get_amc_codes()
       mcoll = self.DB.get_collection('meta')
       for amc_name, amc_code in amc_pairs.items():
         data = amfiparseobj.get_json_from_amc_csvs(amc_name,in_dir)
         if not data:
             continue
         for scheme_code in data[amc_name].keys():
             #scheme_meta = data[amc_name][scheme_code]['meta']
             try:
                 mcoll.insert_one(data[amc_name][scheme_code]['meta'])
             except pymongo.errors.DuplicateKeyError as e:
                 pass
                 #print('{0} : {1}'.format(scheme_code,e))
             scheme_data = data[amc_name][scheme_code]['data']
             collname = 'c'+scheme_code
             if not collname in self.DB.list_collection_names():
                 coll = self.DB.create_collection(collname)
                 coll.create_index([('date',pymongo.ASCENDING)],unique=True)
             else:
                 coll = self.DB.get_collection(collname)
             try:
                 coll.insert_many(scheme_data, ordered=False)
             except pymongo.errors.BulkWriteError as e:
                 print('cannot write: {0}'.format(e))

