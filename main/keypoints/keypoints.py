import json
import sys
import cv2
import os
from sys import platform
import argparse
import numpy as np

def get_video():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', default="./jazz.mp4")
    args = parser.parse_args()
    return args.video



#因為openpose抓到的points若不轉為str會有NoneType和多維處理的問題
#所以使用str並將其格式處理

# def is_none(x):
#     return x=='.' or x=='0.'

def get_format_keypoints(pose):
    frame_keypoints=[]
    if(str(pose)!='None'):
        if len(pose)>1:
            # print("over")
            pose=pose[0]
            # print(pose)
        temp=str(pose)[2:-2]# 扣除前後的2個大括號
        #print(temp)
        temp=temp.split('\n')# 扣除格式化後的\n
        for points in temp:#point為每一frame的一個骨架點#共有25個
            points=points.strip()
            points=points[1:-1]
            points=points.split(' ')
            if '' in points or '.' in points:
                # points=list(filter(is_none,points))
                points=list(filter(None,points))
                #points=list(filter('.',points))
            for point in points:
                #print('ori',point)
                #if point=='.' or point=='0.':
                 #   point='0'
                point=point.replace('[','')
                point=point.replace(']','')
                #print('test',point)
                point=float(point)
            points=list(map(float,points))
            frame_keypoints.append(points)
        return frame_keypoints
    # else:#若是畫面上沒有骨架,則增加都是0的list
    #     return np.zeros((25,3)).tolist()

#import openpose
def main(path):
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            if platform == "win32":
                # Change these variables to point to the correct folder (Release/x64 etc.)
                #前後需要三個資料夾內的東西
                sys.path.append(dir_path + './Release');
                os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + './x64;' +  dir_path + './bin;'
                import pyopenpose as op
                print("success import")

        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e


        # 設定參數
        params = dict()
        # 模型的資料夾
        params["model_folder"] = "./models/"
        # 把每一frame的骨架寫成json #可刪
        #params["write_json"] = "./models/" #資料夾位置指的是json檔放置位置
        
        # 實際使用openpose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # 載入影片 frame
        #video_path=get_video()#取得影片
        video_path='./'+path
        
        total_keypoints=[]#存keypoints,共有 frame數,256,3

        cap = cv2.VideoCapture(video_path)
        c=1
        timeF = 3  #frame頻率   
        print(cap.get(cv2.CAP_PROP_FPS))
        print(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if(cap.isOpened()==False):
            print("Error opening the video stream")
        while(cap.isOpened()):
            ret,frame = cap.read()
            c=c+1
            if(ret==True):
                datum = op.Datum()
                datum.cvInputData=frame
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))
                # print("Body keypoints: \n" + str(datum.poseKeypoints))
                
                total_keypoints.append(get_format_keypoints(datum.poseKeypoints))#將每一個frame的data放至total中
                cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)#畫面上可會顯示東東

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        #print(total_keypoints)#一個影片的所有骨架點yeah
        # with open("keypoints.json","w") as f:
        #     json.dump(total_keypoints, f) 
        output_path='./'+video_path.replace(".mp4","")+".json"
        with open(output_path,"w") as f:
            json.dump(total_keypoints, f) 
        return output_path
    except Exception as e:
        print(e)
        sys.exit(-1)

if __name__ == "__main__":
    print(main(get_video()))