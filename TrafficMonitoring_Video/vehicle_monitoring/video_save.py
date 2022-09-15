import time
import cv2 as cv2
import numpy as np
import collections
import yaml
from azure.storage.blob import ContainerClient

import json
import os
from pathlib import Path
import sys

sys.path.append('..')
from config import PathConfig
input_size = 416

# Detection confidence threshold
confThreshold = 0.2
nmsThreshold = 0.2

font_color = (0, 0, 153)
font_size = 0.6
font_thickness = 3

# Store Coco Names in a list
classesFile = PathConfig.path_coco
classNames = open(classesFile).read().strip().split('\n')

# class index for our required detection classes
required_class_index = [2, 3, 5, 7]

# detected_classNames = []

## Model Files
modelConfiguration = PathConfig.path_config
modelWeigheights = PathConfig.path_weight

# configure the network model
net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeigheights)

# Configure the network backend

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Define random colour for each class
np.random.seed(42)
colors = np.random.randint(0, 255, size=(len(classNames), 3), dtype='uint8')


# In[2]:
def postProcess(outputs, img):
    # global detected_classNames
    height, width = img.shape[:2]
    boxes = []
    classIds = []
    confidence_scores = []
    detection = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if classId in required_class_index:
                if confidence > confThreshold:
                    # print(classId)
                    w, h = int(det[2] * width), int(det[3] * height)
                    x, y = int((det[0] * width) - w / 2), int((det[1] * height) - h / 2)
                    boxes.append([x, y, w, h])
                    classIds.append(classId)
                    confidence_scores.append(float(confidence))

    # Apply Non-Max Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidence_scores, confThreshold, nmsThreshold)

    detected_classNames = []
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]
            name = classNames[classIds[i]]

            detected_classNames.append(name)

            color = [int(c) for c in colors[classIds[i]]]
            name = classNames[classIds[i]]

            # Draw classname and confidence score
            cv2.putText(img, f'{name.upper()} {int(confidence_scores[i] * 100)}%',
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

            # Draw bounding rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            detection.append([x, y, w, h, required_class_index.index(classIds[i])])

    dict1 = dict(collections.Counter(detected_classNames))
    detected_classNames.clear()
    return dict1


# In[3]:


def realTime(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = (cap.get(cv2.CAP_PROP_FPS))
    #print(fps)
    #print(video)
    # out = cv2.VideoWriter('test.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
    dict1 = {"car": 0, "bus": 4, "motorbike": 3, "truck": 4}
    file_name = os.path.basename(video_path)
    video_name= os.path.splitext(file_name)[0]
    print(video_name)
    json_final_list = []
    writer = None
    # frame_count = 0


    while cap.isOpened():
        dict_vehicle = {}
        json_dict = {}
        success, img = cap.read()
        if success:
            # print("frame_count: ",frame_count)
            blob = cv2.dnn.blobFromImage(img, 1 / 255, (input_size, input_size), [0, 0, 0], 1, crop=False)

            # Set the input of the network
            net.setInput(blob)
            # start = time.time()
            layersNames = net.getLayerNames()
            outputNames = [(layersNames[i - 1]) for i in net.getUnconnectedOutLayers()]
            # Feed data to the network
            outputs = net.forward(outputNames)
            
            dict_v = postProcess(outputs, img)
            #print('dict_v',dict_v)

            for i in dict1:
                if i in dict_v:
                    dict_vehicle[i] = dict_v[i]
                else:
                    dict_vehicle[i] = 0

            frame_stamp = (cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000  # condition
            json_dict.update(dict_vehicle)
            json_dict['frame_timestamp'] = frame_stamp
            json_final_list.append(json_dict)
            # print(json_final_list)

            cv2.putText(img, "Car:" + " " + str(dict_vehicle['car']), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                        font_color, font_thickness)
            cv2.putText(img, "Bus:" + " " + str(dict_vehicle['bus']), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                        font_color, font_thickness)
            cv2.putText(img, "Truck:" + " " + str(dict_vehicle['truck']), (20, 80), cv2.FONT_HERSHEY_SIMPLEX, font_size,
                        font_color, font_thickness)
            cv2.putText(img, "Motorbike:" + " " + str(dict_vehicle['motorbike']), (20, 100), cv2.FONT_HERSHEY_SIMPLEX,
                        font_size, font_color, font_thickness)
            dict_vehicle.clear()

            cv2.imshow('output', img)
            if writer is None:
                resultVideo = cv2.VideoWriter_fourcc(*'vp80')

                output_path = PathConfig.BASE_DIR + PathConfig.OUTPUT_DIR
                writer = cv2.VideoWriter(output_path +video_name+'.webm', resultVideo, 30,
                                         (img.shape[1], img.shape[0]), True)

            # Write processed current frame to the file
            writer.write(img)
            c = cv2.waitKey(1)
            if c & 0xFF == ord('q'):
                break
        else:
            break
        # frame_count += 1
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
   
    output_path =  PathConfig.OUTPUT_DIR+video_name+'.webm'
    json_list_final = []
    for i in range(0, len(json_final_list), int(fps)):
        # print(i)
        k = json_final_list[i]
        #print(k)
        json_list_final.append(k)
    return json_list_final, output_path
