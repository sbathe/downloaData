#!/usr/bin/env python3
from amfi import AmfiDownload
from amfi import AmfiParse
import pymongo, datetime, re

class AmfiMongo:
    def __init__(self):
        # pull config data here
        client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
        self.DB = client.amfi
        if not 'meta' in self.DB.list_collection_names():
            self.mcoll = self.DB.create_collection('meta')
            self.mcoll.create_index([('scheme_code',pymongo.ASCENDING)],unique=True)
            self.mcoll.create_index([('name', pymongo.TEXT), ('amc',pymongo.TEXT)])
        if not 'data' in self.DB.list_collection_names():
            self.dcoll = self.DB.create_collection('data')
            self.dcoll.create_index([('scheme_code',pymongo.ASCENDING), ('date',pymongo.ASCENDING)],unique=True)
        if not 'amcs' in self.DB.list_collection_names():
           self.amccoll = self.DB.create_collection('amcs')
           self.amccoll.create_index([('name', pymongo.TEXT)])

    def write_amc_pairs(self):
        amfidownloadobj = AmfiDownload()
        amc_pairs = amfidownloadobj.get_amc_codes()
        amcs = [k for k,v in amc_pairs.items()]
        for e in amcs:
            self.amccoll.insert_one({'name': e})



    def write_jsons_to_docments(self, in_dir):
       amfidownloadobj = AmfiDownload()
       amfiparseobj = AmfiParse()
       amc_pairs = amfidownloadobj.get_amc_codes()
       mcoll = self.DB.get_collection('meta')
       dcoll = self.DB.get_collection('data')
       for amc_name, amc_code in amc_pairs.items():
         data = amfiparseobj.get_json_from_amc_csvs(amc_name,in_dir)
         if not data:
             continue
         for scheme_code in data[amc_name].keys():
             #scheme_meta = data[amc_name][scheme_code]['meta']
             if re.search('direct',data[amc_name][scheme_code]['meta']['name'],re.IGNORECASE):
                 try:
                     mcoll.insert_one(data[amc_name][scheme_code]['meta'])
                 except pymongo.errors.DuplicateKeyError as e:
                     pass
                     #print('{0} : {1}'.format(scheme_code,e))
                 scheme_data = data[amc_name][scheme_code]['data']
                 #collname = 'c'+scheme_code
                 #if not collname in self.DB.list_collection_names():
                 #    coll = self.DB.create_collection(collname)
                 #    coll.create_index([('date',pymongo.ASCENDING)],unique=True)
                 #else:
                 #    coll = self.DB.get_collection(collname)
                 try:
                     dcoll.insert_many(scheme_data, ordered=False)
                 except pymongo.errors.BulkWriteError as e:
                     print('cannot write: {0}'.format(e))

    def find_min_date_for_scheme(self, scheme_code):
        r = self.dcoll.find_one({'scheme_code': scheme_code},sort=[('date', 1)])
        return r['date']

    def find_max_date_for_scheme(self, scheme_code):
        r = self.dcoll.find_one({'scheme_code': scheme_code},sort=[('date', -1)])
        return r['date']

    def get_scheme_code_from_name(self, name):
        r = self.mcoll.find({'name': name})
        return r['scheme_code']

    def get_details_for_scheme_code(self,scheme_code):
        r = self.mcoll.find({'scheme_code': str(scheme_code)})
        return r

    def get_fundnames_from_text(self, text):
        rs = dict()
        rs['names'] = list()
        for r in self.mcoll.find({'$text': {'$search': 'value'}}):
            rs.append(r['name'])
        return rs

    def get_scheme_navs_between_dates(self,scheme_code,start_date=None,end_date=None):
        if not start_date:
            start_date = self.find_min_date_for_scheme(scheme_code)
        if not end_date:
            end_date = self.find_max_date_for_scheme(scheme_code)
        ds = dict()
        ds['data'] = list()
        for e in self.dcoll.find({'$and': [{'date': { '$gte': start_date}}, {'date': {'$lte': end_date}}, {'scheme_code':scheme_code}]},{'_id': False, 'date': True, 'nav': True}):
            ds['data'].append(e)
       return ds
