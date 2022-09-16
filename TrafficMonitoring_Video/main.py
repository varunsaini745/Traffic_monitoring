import json
from fastapi import FastAPI, UploadFile, File
from vehicle_monitoring.video_save import realTime
import shutil
import os
from config import PathConfig
from database import Database
from pydantic import BaseModel

DB = Database()
app = FastAPI()
#ROOT_DIR = os.path.abspath(os.curdir)

class Item(BaseModel):
    file:str
    uuid:str

@app.post('/')
def root(input:Item):
    uuid = input.uuid
    # return False
    try:
        #print('base directory:',PathConfig.BASE_DIR)
        dir_root = os.getcwd()
        dir_root = dir_root.replace('\\', '/')
        input_file = dir_root+'/data/'+input.file
        input_path = input.file
        status = 'running'
        #(self,id,status,input_path,output_path= None, json_count=None) 
        #update(self,id,output_path,status,json_count,input_path=None)
        response = DB.insert(uuid,status, input_path)
        if not response:
            pass
            # need to add log file
        json_count, output_path=realTime(input_file, dir_root)
        print(json_count)
        # _,output_path=weapon_detection(input_file)
        if json_count:
            status='Success'
            response = DB.update(uuid,output_path,status,json_count)
            return {
                "status": "Success",
                "filepath": output_path,
                "Error": ''}
        else:
            raise Exception(output_path)

    except Exception as e:
        status = f"Error {str(e)}"
        db_update = DB.update(uuid,"",status)
        return {"status": "Error",
                "filepath": "",
                "Error": str(e) }


@app.get('/health')
def get_health_status():
    return {'message': "API is working"}

#if __name__ == '__main__':
    