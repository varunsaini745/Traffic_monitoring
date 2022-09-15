class PathConfig:
    BASE_DIR = 'C:/Users/VarunSaini/OneDrive - Audax Labs Private Limited/TrafficMonitoring_Video/data/'
    INPUT_DIR = 'traffic_monitoring/input/'
    OUTPUT_DIR = 'traffic_monitoring/output/'
    path_coco = 'C:/Users/VarunSaini/OneDrive - Audax Labs Private Limited/TrafficMonitoring_Video/vehicle_monitoring/coco.names'
    path_weight= 'C:/Users/VarunSaini/OneDrive - Audax Labs Private Limited/TrafficMonitoring_Video/vehicle_monitoring/yolov4.weights'
    path_config = 'C:/Users/VarunSaini/OneDrive - Audax Labs Private Limited/TrafficMonitoring_Video/vehicle_monitoring/yolov4.cfg'
# /model/yolov4_train_last_latest.weights", r".

class DatabaseConfig:
    server = "mongodb+srv://varun:varunvarun@cluster0.ixxzfv2.mongodb.net/?retryWrites=true&w=majority"
    database_name = "vehicle_monitoring"
    database_collection = "background"
    database_col_result = "vehicle_result"
   
