# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 17:23:34 2022

@author: VarunSaini
"""
import pymongo
myclient = pymongo.MongoClient('mongodb+srv://varun:varunvarun@cluster0.ixxzfv2.mongodb.net/?retryWrites=true&w=majority')
print(myclient)
my_db = myclient['vehicle-monitoring']
my_col = my_db['vehcile_result']
my_db_schema = {
               "uuid": "890976543agh",
               "filename": "accident",
               "filepath":"",
               "thumbnail_path":"",
               "status": "" }
my_col.insert_one(my_db_schema)