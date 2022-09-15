# import pymongo
import sys
sys.path.append("..")
import pymongo
from pymongo import MongoClient
from config import DatabaseConfig
import pprint
import datetime


class Database:
    def __init__(self) -> None:
        self.myclient = pymongo.MongoClient(DatabaseConfig.server)
        self.my_db = self.myclient[DatabaseConfig.database_name]
        self.my_col = self.my_db[DatabaseConfig.database_collection]
        self._db_schema ={
                   "uuid": "", 
                   "input_path": "",
                   "output_path":"", 
                   "status":"",
                   "json_count": "",
                   "last_modified":datetime.datetime.now().astimezone().isoformat()
        }

    def insert(self,id,status,input_path,output_path= None, json_count=None) -> bool:
        get_data = self.get(id)
        if get_data is not None:
            return False
        self._db_schema ={
                   "uuid": id, 
                   "status":status,
                   "input_path": input_path,
                   "output_path":output_path, 
                   "json_count": json_count,
                   "last_modified":datetime.datetime.now().astimezone().isoformat()
        }  
        self.my_col.insert_one(self._db_schema)
        return True
         

    def update(self,id,output_path,status,json_count,input_path=None):
        get_data = self.get(id)
        if get_data is None:
            return False
        if input_path is None:
            f = {"uuid": id}
            values = {"$set":{"output_path":output_path,
                            "status":status,
                            "json_count":json_count,
                            "last_modified":datetime.datetime.now().astimezone().isoformat()
                            }}
            self.my_col.update_one(f,values)
            return True
        else:
            return False


    def get(self,id):
        entity = self.my_col.find_one({'uuid':id})
        return entity

#if __name__=="__main__":
    #d = Database()
    #data = d.insert("05a4f048-9a40-4aac-9a49-a90a819f588891","","pending","weapon_detection_processing/input/new_222.mp4")
    # data = d.get("05a4f048-9a40-4aac-9a49-a90a819f5888")
    # del data['_id']
    # pprint.pprint(json.dumps(data))
    # data = d.update("05a4f048-9a40-4aac-9a49-a90a819f5888","","Pending")
    # mydict = { "uuid": "@dgdfs@$@@", "Input_path": "xyz.mp4","Output_path":"xyz.avi", "status":"Pending" }
    # x = mycol.insert_one(mydict)