from midi2audio import FluidSynth
from pydub import AudioSegment
from moviepy.editor import *
import random



def conversion(src,dst):
    fs = FluidSynth()
    fs.midi_to_audio(src, dst)


def slice(path,duration):
    song = AudioSegment.from_wav(path)
    num=random.randint(4, 9)
    start=(num)*1000
    end=(num+duration)*1000
    save_path=path[:-4]+'_slice'+str(num)+'.mp3'
    song[start:end].export(save_path) 
    return save_path


def clipMusic(file):
    file=file
    sound=[]
    for i in range(len(file)):
        sound.append(AudioSegment.from_mp3(file[i]))
    finSound=sound[0]
    for i in range(1,len(sound)):
        finSound += sound[i]
    save_path = file[0][:-11]+'_end.mp3'
    print("final audio saved:", save_path)
    finSound.export(save_path, format="mp3", tags={'artist': 'musicbox', 'album': save_path[:-4]})
    return save_path


def videoAudioClip(video,audio):
    audioclip = AudioFileClip(audio)
    clip = VideoFileClip(video)
    new_video = clip.set_audio(audioclip)
    save_path=video[:-4]+'_end.mp4'
    new_video.write_videofile(save_path)
    print("final audio saved:", save_path)
    return save_path


def mediaClip(duration,filepaths,dance_path):

    # TODO: duration
    # duration=duration
    slice_duration=10

    # TODO: generating music path
    path = filepaths
    index = len(path) - 1

    for i in range(len(path)):
        dst=path[i][:-4]+'.wav'
        conversion(path[i], dst)
        if i == index:
            slice_duration = 10 + duration % 10
        path[i] = slice(dst,slice_duration)
    
    # TODO: input video path
    video = './' + dance_path
    audio = clipMusic(path)
    videoPath = videoAudioClip(video, audio)
    # TODO: return final audio & video
    return audio,videoPath


