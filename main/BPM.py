import json
import matplotlib.pyplot as plt
import librosa
import argparse
import numpy as np
import math
import shutil
import mido
import pretty_midi
from mido import MidiFile,MetaMessage


# def get_json(input_json):#傳入骨架點的json檔案
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--json', default=input_json)
#     args = parser.parse_args()
#     return args.json

def getAngle(point1_x,point1_y,point2_x,point2_y):
    """
    取得兩點間的角度
    :param point1_x:
    :param point1_y:
    :param point2_x:
    :param point2_y:

    :return: insideAngle:角度
    """

    dx1 = 0 - point1_x
    dy1 = 0 - point1_y
    dx2 = 0 - point2_x
    dy2 = 0 - point2_y

    angle1 = math.atan2(dy1, dx1)
    angle1 = int(angle1 * 180 / math.pi)
    # print(angle1)
    angle2 = math.atan2(dy2, dx2)
    angle2 = int(angle2 * 180 / math.pi)
    # print(angle2)
    if angle1 * angle2 >= 0:
        insideAngle = abs(angle1 - angle2)
    else:
        insideAngle = abs(angle1) + abs(angle2)
        if insideAngle > 180:
            insideAngle = 360 - insideAngle
    insideAngle = insideAngle % 180
    return insideAngle

def saveAngle(keypoints):
    """
    抓要計算角度的節點
    :param keypoints:原骨架點

    :return: keypoints:增加角度後的骨架點
    """

    #把原本是信心水準的z變成0
    for i in range(len(keypoints)):
        for j in range(len(keypoints[i])):
            if keypoints[i][j]==[]:
                keypoints[i][j]=[0,0,0]
            else:
                keypoints[i][j][2]=0

    #可以順便把角度丟到z XD
    for i in range(len(keypoints)):
        #脖子至兩肩
        keypoints[i][2][2]=getAngle(keypoints[i][1][0],keypoints[i][1][1],keypoints[i][2][0],keypoints[i][2][1])
        # print(keypoints[i][2][2])
        keypoints[i][5][2]=getAngle(keypoints[i][1][0],keypoints[i][1][1],keypoints[i][5][0],keypoints[i][5][1])
        
        #兩肩至兩肘
        keypoints[i][3][2]=getAngle(keypoints[i][2][0],keypoints[i][2][1],keypoints[i][3][0],keypoints[i][3][1])
        keypoints[i][6][2]=getAngle(keypoints[i][5][0],keypoints[i][5][1],keypoints[i][6][0],keypoints[i][6][1])

        #兩肘至兩腕
        keypoints[i][4][2]=getAngle(keypoints[i][3][0],keypoints[i][3][1],keypoints[i][4][0],keypoints[i][4][1])
        keypoints[i][7][2]=getAngle(keypoints[i][6][0],keypoints[i][6][1],keypoints[i][7][0],keypoints[i][7][1])
        #---
        #胯下至兩臀
        keypoints[i][9][2]=getAngle(keypoints[i][8][0],keypoints[i][8][1],keypoints[i][9][0],keypoints[i][9][1])
        keypoints[i][12][2]=getAngle(keypoints[i][8][0],keypoints[i][8][1],keypoints[i][12][0],keypoints[i][12][1])
        
        #兩臀至兩膝
        keypoints[i][10][2]=getAngle(keypoints[i][9][0],keypoints[i][9][1],keypoints[i][10][0],keypoints[i][10][1])
        keypoints[i][13][2]=getAngle(keypoints[i][12][0],keypoints[i][12][1],keypoints[i][13][0],keypoints[i][13][1])
        
        #兩膝至兩踝
        keypoints[i][11][2]=getAngle(keypoints[i][10][0],keypoints[i][10][1],keypoints[i][11][0],keypoints[i][11][1])
        keypoints[i][14][2]=getAngle(keypoints[i][13][0],keypoints[i][13][1],keypoints[i][14][0],keypoints[i][14][1])
        
        # print(keypoints[i])

        return keypoints

def sumOfKeypoints(keypoints):

    """
    將t時間點的25個點，與t-1時間點的取差值後相加(每一frame的總骨架點差值數)->(frame數,3)
    :param keypoints:原骨架點(frame數，25個點，xy值及信心水準)
    :return: sum_keypoints:每一frame的總骨架點差值數
    """

    sum_keypoints=[]
    for i in range(len(keypoints)-1,0,-1):#frame數
        frame=[0.0,0.0,0.0]
        for j in range(len(keypoints[i])):#25
            for k in range(len(keypoints[i][j])):
                if i==0:
                    frame[k]=keypoints[i][j][k]
                else:
                    frame[k]=frame[k]+abs(keypoints[i][j][k]-keypoints[i-1][j][k])
        sum_keypoints.append(frame)
    return sum_keypoints

def diffOfKeypoints(sum_keypoints):
    """
    取t,t-1時間差值
    :param sum_keypoints:每一frame的總骨架點差值數
    :return: normalize_keypoints:取t,t-1差值後正規化
    """
    diff_keypoints=[]
    for i in range(len(sum_keypoints)-1,0,-1):
        diff_frame=[0.0,0.0,0.0]
        for j in range(len(sum_keypoints[i])):
            if i==0:
                diff_frame[j]=sum_keypoints[i][j]
            else:
                diff_frame[j]=abs(sum_keypoints[i][j]-sum_keypoints[i-1][j])
        diff_keypoints.append(diff_frame)
    normalize_keypoints=librosa.util.normalize(diff_keypoints)
    return normalize_keypoints

def maxbeats(normalize_keypoints_temp):
    """
    取正規化後的值取最大的1/5
    :param normalize_keypoints_temp:正規化後的骨架點
    :return: beats_index:最大的1/5的index
    """
    beats_index=[]
    for i in range(int(len(normalize_keypoints_temp)/5)):
        max1=np.argmax(normalize_keypoints_temp)
        beats_index.append(max1)
        normalize_keypoints_temp[max1]=-1 #將大值改為-1
    # print(len(beats_index))
    beats_index.sort()#因為大值的index順序不順，所以將其排序
    # print(beats_index)
    return beats_index

def diff_index(beats_index):
    """
    取正規化後的值取最大的1/5
    :param normalize_keypoints_temp:正規化後的骨架點
    :return: beats_index:最大的1/5的index
    """
    diff=0
    number=0
    biggest=0
    index=-1
    for i in range(len(beats_index)-1,0,-1):
        if i !=0:
            diff_number=beats_index[i]-beats_index[i-1]
            if diff_number!=1:
                next_index=beats_index[i]
                pre=beats_index[i]
                j=1
                while next_index <= len(beats_index) or pre>=0:
                    next_index=beats_index[i]+diff_number*j
                    pre=beats_index[i]-number*j
                    if next_index in beats_index:
                        number=number+1
                    if pre in beats_index:
                        number=number+1
                #     print(next_index)
                #     print(pre)
                    j=j+1
            if biggest<number:
                biggest=number
                index=beats_index[i]
                diff=diff_number
    return index,diff

def build_times(start,beat,len_index):
    """
    建立節奏點時間列表
    :param start:開始預設0，一開始就有動作
    :param beat:隔幾個index
    :param len_index:index長度

    :return index:節奏點index list
    :return times:節奏點時間list 

    """
    times=[]
    times.append(start)
    i=1
    next_index=start
    pre=start
    while next_index <=len_index or pre>=0:
        next_index=start+beat*i
        pre=start-beat*i
    #     print(next_index)
    #     print(pre)
        if next_index<=len_index:
            times.append(next_index)
        if pre>=0:
            times.append(pre)
        i=i+1
    times.sort()
    # print(times)
    index=times
    for i in range(len(times)):
        times[i]=times[i]/25
#     print(times)
#     print(len(times))
    return index,times

def basetofind(plus,len_index,beats_index_x,beats_index_y,beats_index_z):
    """
    建立節奏點時間列表
    :param plus:增加的數字
    :param beats_index_x:x的1/5大值的index
    :param beats_index_y:y的1/5大值的index
    :param beats_index_z:z的1/5大值的index

    """
    tempo_plus=120+plus
    tempo_minus=120-plus

    frequency_minus=0
    frequency_plus=0

    index_plus=int(25/(tempo_plus/60))
    index_minus=int(25/(tempo_minus/60))

    #取時間陣列
    index_list_plus,times_plus=build_times(0,index_plus,len_index)#取120上下的
    index_list_minus,times_minus=build_times(0,index_minus,len_index)

    for i in beats_index_x:
        if i in index_list_plus:
            frequency_plus=frequency_plus+1
        if i in index_list_minus:
            frequency_minus=frequency_minus+1

    for i in beats_index_y:
        if i in index_list_plus:
            frequency_plus=frequency_plus+1
        if i in index_list_minus:
            frequency_minus=frequency_minus+1

    for i in beats_index_z:
        if i in index_list_plus:
            frequency_plus=frequency_plus+1
        if i in index_list_minus:
            frequency_minus=frequency_minus+1
    
    return index_plus,frequency_plus,tempo_plus,index_minus,frequency_minus,tempo_minus

def basetofind2(len_index,beats_index_x,beats_index_y,beats_index_z):

    """
    :param beats_index_x:x的1/5大值的index
    :param beats_index_y:y的1/5大值的index
    :param beats_index_z:z的1/5大值的index

    :return save[0][0]:beats_index
    :return save[0][2]:beats per minutes
    """

    plus=0
    stop=False
    save=[[0,0,0]]
    while not stop:
        index_plus,frequency_plus,tempo_plus,index_minus,frequency_minus,tempo_minus=basetofind(plus,len_index,beats_index_x,beats_index_y,beats_index_z)
        if frequency_minus < save[0][1] and frequency_plus < save[0][1]:
            stop=True
        else:
            if frequency_plus < frequency_minus:
                save[0][0]=index_minus
                save[0][1]=frequency_minus
                save[0][2]=tempo_minus
            else:
                save[0][0]=index_plus
                save[0][1]=frequency_plus
                save[0][2]=tempo_plus
        plus=plus+1
    return save[0][0],save[0][2]

def beat_main(input_json):

    # json_file=get_json(input_json)
    json_file=input_json
    with open(json_file,"r") as f:
        keypoints = json.load(f)
    # print(keypoints)
    keypoints=saveAngle(keypoints)

    sum_keypoints=sumOfKeypoints(keypoints)
    # print(sum_keypoints)
    normalize_keypoints=diffOfKeypoints(sum_keypoints)

    normalize_keypoints_x=[]
    normalize_keypoints_y=[]
    normalize_keypoints_z=[]
    for i in normalize_keypoints:
        normalize_keypoints_x.append(i[0])
        normalize_keypoints_y.append(i[1])
        normalize_keypoints_z.append(i[2])
    # print(normalize_keypoints_z)

    beats_index_x=maxbeats(normalize_keypoints_x)
    beats_index_y=maxbeats(normalize_keypoints_y)
    beats_index_z=maxbeats(normalize_keypoints_z)

    beat,tempo=basetofind2(len(keypoints),beats_index_x,beats_index_y,beats_index_z)
    # print(beat)
    # print(tempo)
    index,times=build_times(0,beat,len(keypoints))
    return times,tempo,tempo/60


def get_tempo(path):
    pm = pretty_midi.PrettyMIDI(path)
    tempo_estimated = pm.estimate_tempo()
    _, tempo = pm.get_tempo_changes()
    return tempo.tolist()

def get_path(filename):
    src=filename
    dst=src[:-4]+'_bpm.mid'
    # print(src,dst)
    shutil.copyfile(src, dst)
    return src,dst


def set_tempo(filename,bpm):
    src,dst=get_path(filename)
    src_mid=mido.MidiFile(src)
    dst_midi=mido.MidiFile(dst)
    dst_tempo=mido.bpm2tempo(bpm)
    for i, track in enumerate(src_mid.tracks):
        # print('Track {}: {}'.format(i, track.name))
        new_track = mido.MidiTrack()
        new_track.name = track.name
        for message in track:
            if isinstance(message, MetaMessage):
                if message.type == 'set_tempo':
                    message= mido.MetaMessage('set_tempo', tempo=dst_tempo)
                    new_track.append(message)
        dst_midi.tracks.append(new_track)
    
    dst_midi.save(dst)

    pm = pretty_midi.PrettyMIDI(dst)
    return dst
    # print(get_tempo(src), get_tempo(dst))


def tempo(filename, input_json):
    print("---caculating tempo---")
    time_list,bpm,bps=beat_main(input_json)
    dst=set_tempo(filename,bpm)
    return dst


# if __name__ == "__main__":



