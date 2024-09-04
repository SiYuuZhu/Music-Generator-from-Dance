import json
import argparse
from dtaidistance import dtw_ndim
import numpy as np


dance_style = {0:"tango",1:"jazz",2:"chacha",3:"NONE"}

JsonSet=[
    ["./Tango/tango1.json","./Tango/tango2.json","./Tango/tango3.json","./Tango/tango4.json","./Tango/tango5.json"]
    ,["./Jazz/jazz1.json","./Jazz/jazz2.json","./Jazz/jazz3.json","./Jazz/jazz4.json","./Jazz/jazz5.json"]
    ,["./Chacha/chacha1.json","./Chacha/chacha2.json","./Chacha/chacha3.json","./Chacha/chacha4.json","./Chacha/chacha5.json"]
]
JsonSet = np.array(JsonSet)


def get_dtw(input_json):
    input_json = get_inputjson(input_json)
    min_dtw = 2000
    style = 2
    startframe = 0
    intervalframe = 250
    styles = []
    if len(input_json) < intervalframe:
        for JsonData in JsonSet:
            for file_name in JsonData:
                y = get_json(file_name)
                dtw_total,frame = 0,0
                if len(input_json)<=125:
                    interval=len(input_json)
                else:
                    interval=len(y)
                while startframe + frame + interval <= endframe:
                    dist = dtw_ndim.distance(input_json[startframe+frame:startframe+frame+interval],y)
                    frame+=5
                    dtw_total+= dist
                    if dist < min_dtw:
                        min_dtw = dist
                        style = int(np.where(JsonSet==file_name)[0])
                    if dist == 0:
                        min_dtw = dist
                        style = int(np.where(JsonSet==file_name)[0])
                        print("---與特徵檔為同種舞風---")
                        break
                print("與{0}特徵檔比對的DTW平均：{1}".format(dance_style.get(int(np.where(JsonSet == file_name)[0])),dtw_total/(frame//5)))
        startframe+= intervalframe
        styles.append(dance_style.get(style))
    else:
        while startframe + intervalframe <= len(input_json):
            endframe = startframe + intervalframe
            for JsonData in JsonSet:
                for file_name in JsonData:
                    y = get_json(file_name)
                    dtw_total,frame = 0,0
                    if len(input_json)<=125:
                        interval=len(input_json)
                    else:
                        interval=len(y)
                   
                    while startframe + frame + interval <= endframe:
                        dist = dtw_ndim.distance(input_json[startframe+frame:startframe+frame+interval],y)
                        frame+=5
                        dtw_total+= dist
                        if dist < min_dtw:
                            min_dtw = dist
                            style = int(np.where(JsonSet==file_name)[0])
                        if dist == 0:
                            min_dtw = dist
                            style = int(np.where(JsonSet==file_name)[0])
                            print("---與特徵檔為同種舞風---")
                            break
                    print("與{0}特徵檔比對的DTW平均：{1}".format(dance_style.get(int(np.where(JsonSet == file_name)[0])),dtw_total/(frame//5)))
            startframe+= intervalframe
            styles.append(dance_style.get(style))
    return styles



def get_inputjson(file_name):
    # file_name = "./Tango/"+file_name
    with open(file_name, 'r') as obj:
        # data = np.array(json.load(obj))
        data = np.array(json.load(obj))[:,:,:2]
        data = np.delete(data,[0,1,15,16,17,18,19,20,21,22,23,24],axis=1)
        origin = data[0][6].copy()

        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = data[i][j] - origin
        
    return data

def get_json(file_name):
    with open(file_name, 'r') as obj:
        data = np.array(json.load(obj))
    return data

def rewrite_json(file_name):
    with open(file_name, 'r') as obj:
        data = np.array(json.load(obj))[:,:,:2]
        data = np.delete(data,[0,1,15,16,17,18,19,20,21,22,23,24],axis=1)
        origin = data[0][6].copy()
        for i in range(len(data)):
            for j in range(len(data[i])):
                data[i][j] = data[i][j] - origin
                print(data[i][j])
        listdata = data.tolist() 
        for i in range(0,len(listdata)):
            for j in range(0,len(listdata[i])):
                for k in range(0,len(listdata[i][j])):                
                    listdata[i][j][k] = float("%.4f" % listdata[i][j][k])
    with open(file_name,"w", encoding='utf-8') as obj:
        json.dump(listdata, obj)
