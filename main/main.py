
from . import keypoints
from .music_vae import music_vae_generate
from . import DTW_compare
from . import BPM
from . import clip


def origin():
    input_json = keypoints.main('tango1.mp4')
    style = DTW_compare.get_dtw(input_json)
    filename = music_vae_generate.console_entry_point(style)
    BPM.tempo('./music_vae/generate/interpolate/'+filename,input_json)
    print('finish')

def generate(dance_path, music_id):
    input_json,duration = keypoints.main(dance_path)
    style = DTW_compare.get_dtw(input_json)
    print(style)
    filepaths = generate_music(style,str(music_id))
    for i in range(len(filepaths)):
        filepaths[i]=BPM.tempo(filepaths[i],input_json)
    audio,video=clip.mediaClip(duration,filepaths,dance_path)
    return audio,video

def generate_music(styles: [str], music_id: str) -> [str]:
    seed_midi = {'jazz': './music_vae/generate/jazz_music/AfterYou_extract.mid',
                 'tango': './music_vae/generate/tango_music/DonPedro.mid',
                 'chacha': './music_vae/generate/chacha_music/chacha_extract.mid'}
    filepaths = []  # music_id_0.mid, music_id_1.mid, music_id_2.mid

    for i,style in enumerate(styles):  # 根據更格變換決定前後midi
        input_midi_1, input_midi_2 = '', ''
        if i == 0:
            input_midi_1 = seed_midi[style]
        else:
            input_midi_1 = filepaths[i-1]
        
        if i == len(styles)-1:
            input_midi_2 = seed_midi[style]
        else:
            input_midi_2 = seed_midi[styles[i+1]]
        
        filepath = './music_vae/generate/interpolate/' + music_vae_generate.console_entry_point(input_midi_1, input_midi_2, music_id+'_'+str(i))
        filepaths.append(filepath)
        print('generate music', i)

    return filepaths
    

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--style', type=str, default=None)
    # args = parser.parse_args()
    pass