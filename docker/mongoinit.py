#!/usr/bin/env python3
from pymongo import MongoClient
import json
client = MongoClient()
db = client.admin
db.command("createUser", "root", pwd='password',roles=['root'])
db.command("createUser", "useradmin",pwd="userAdmin", roles=['readWriteAnyDatabase','dbAdminAnyDatabase','clusterAdmin','userAdminAnyDatabase'])
portfolio = client.portfolio
portfolio.command("createUser", "pfadmin", pwd="pfuserpwd", roles=['dbOwner'])
portfolio.create_collection('users')
portfolio.create_collection('folios')
p = json.load(open('portfolio.json'))
portfolio.folios.insert(p)
portfolio.folio.create_index('username')
