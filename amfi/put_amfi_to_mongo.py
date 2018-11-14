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
             scheme_meta = data[amc_name][scheme_code]['meta']
             scheme_data = data[amc_name][scheme_code]['data']
             collname = 'c'+scheme_code
             if not collname in self.DB.list_collection_names():
                 coll = self.DB.create_collection(collname)
                 for ufield in ['date']:
                     coll.create_index([(ufield,pymongo.ASCENDING)],unique=True)
                 for field in ['scheme_code', 'name']:
                     coll.create_index(field)
                 coll.insert_one(scheme_meta)
             else:
                 coll = self.DB.get_collection(collname)
             for element in data[amc_name][scheme_code]['data']:
                 d = element['date']
                 element['date'] = datetime.datetime.strptime(d,'%d-%b-%Y')
                 try:
                     coll.insert_one(element)
                 except pymongo.errors.DuplicateKeyError as e:
                     print('{0} : {1}'.format(element,e))
       """
       for amc_name, amc_code in amc_pairs.items():
           data = amfiparseobj.get_json_from_amc_csvs(amc_name,in_dir)
           print(type(data))
           if not data:
               continue
           for scheme_code in data[amc_name].keys():
               meta = data[amc_name][scheme_code]['meta']
               data = data[amc_name][scheme_code]['data']
               collname = 'c'+scheme_code
               ### get a new method
               if not collname in self.DB.list_collection_names():
                 coll = self.DB.create_collection(collname)
                 for field in ['scheme_code','date', 'name']:
                   coll.create_index([field],unique=True)
                 coll.insert_one(meta)
               else:
                 coll = self.DB.get_collection(collname)
               ### end get a new method
               #coll.update_one({"scheme_code": scheme_code},{"$set": {"meta": meta}}, True)
               # data is not getting inserted at all
               try:
                   coll.insert_many(data,ordered=False)
               except pymongo.errors.BulkWriteError:
                   pass
    """
