import json
import scipy
from dtaidistance import dtw_ndim
import numpy as np
from scipy.spatial.distance import euclidean
import time 
from tqdm import tqdm
from time import sleep

t1=time.time()
parser = argparse.ArgumentParser()
parser.add_argument('--input_file', default = "./jazz.json")
args = parser.parse_args()

dance_style = {0:"tango",1:"jazz",2:"chacha",3:"NONE"}

JsonSet=[
    ["./Tango/tango1.json","./Tango/tango2.json","./Tango/tango3.json","./Tango/tango4.json","./Tango/tango5.json"]
    ,["./Jazz/jazz1.json","./Jazz/jazz2.json","./Jazz/jazz3.json","./Jazz/jazz4.json","./Jazz/jazz5.json"]
    ,["./Chacha/chacha1.json","./Chacha/chacha2.json","./Chacha/chacha3.json","./Chacha/chacha4.json","./Chacha/chacha5.json"]
]
JsonSet = np.array(JsonSet)

def get_dtw(input_json):
    min_dtw=1000
    style=3
    for JsonData in JsonSet:
        for file_name in JsonData:
            y=get_json(file_name)
            dtw_total,frame = 0,0
            if len(input_json)<=125:
                interval=len(input_json)
            else:
                interval=len(y)
            # progress_total = (len(input_json)- len(y)) //5 +1  
            # progress = tqdm(total = progress_total, desc = "與{}特徵檔比對進度".format( dance_style.get(int(np.where(file_name)[0]))))
            # print(progress_total)
            while frame+interval <= len(input_json):
                
                dist = dtw_ndim.distance(input_json[frame:frame+interval],y)
                frame+=5
                # print("第{0}次DTW結果:{1}".format(frame//5,dist))
                # progress.update(1)
                dtw_total+= dist
                if dist < min_dtw:
                    min_dtw = dist
                    style = int(np.where(JsonSet==file_name)[0])
                if dist==0:
                    # progress.update(progress_total-(frame/5))
                    # print(progress_total,"frame",frame)
                    print("---與特徵檔為同種舞風---")
                    break
            print("與{0}特徵檔比對的DTW平均：{1}".format(dance_style.get(int(np.where(JsonSet == file_name)[0])),dtw_total/(frame//1)))
    return style

def get_json(file_name):
    with open(file_name, 'r') as obj:
        # data = np.array(json.load(obj))
        data = np.array(json.load(obj))[:,:,:2]
    return np.delete(data,[0,1,8,15,16,17,18,19,20,21,22,23,24],axis=1)

    
file=args.input_file
with open(file, 'r') as obj:
    data = json.load(obj)

x=np.array(data)[:,:,:2]
x=np.delete(x,[0,1,8,15,16,17,18,19,20,21,22,23,24],axis=1)
print("input的長度為:",len(x))
result = dance_style.get(get_dtw(x))
if result == "NONE":
    print("請重新載入影片")
else:
    print("此影片最最相近舞風為:{}".format(result))

# print("此影片最最相近舞風為:{}".format(dance_style.get(get_dtw(x))))

t2=time.time()
print("time cost:" + str(round(t2-t1,2)))
