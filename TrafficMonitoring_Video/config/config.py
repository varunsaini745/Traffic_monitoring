import os

class PathConfig:
    #BASE_DIR = 'C:/Users/VarunSaini/OneDrive - Audax Labs Private Limited/TrafficMonitoring_Video/data/'
    INPUT_DIR = 'traffic_monitoring/input/'
    OUTPUT_DIR = 'traffic_monitoring/output/'


class DatabaseConfig:
    server = "mongodb+srv://varun:varunvarun@cluster0.ixxzfv2.mongodb.net/?retryWrites=true&w=majority"
    database_name = "vehicle_monitoring"
    database_collection = "background"
    database_col_result = "vehicle_result"
   
