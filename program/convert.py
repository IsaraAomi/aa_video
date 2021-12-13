import os, glob, re
from tqdm import tqdm
from multiprocessing import Pool
from moviepy.editor import *

from opencv_video_to_still import *
from AA import *
from args import *


# tqdm's bar_format
short_progress_bar="{l_bar}{bar:10}{r_bar}{bar:-10b}"


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]


def get_flist(dir, ext):
    """
    - Args:
        - dir (str)
        - ext (str)
    - Returns:
        - flist (list)
    """
    flist = sorted(glob.glob(os.path.join(dir, '*.'+ext)), key=natural_keys)
    return flist


def get_text_size(text_path):
    """
    - Args:
        - text_path (str)
    - Returns:
        - width (int)
        - height (int)
    """
    with open(text_path) as f:
        text_list = f.readlines()
        width = len(text_list[0]) - 1
        height = len(text_list)
    return width, height


def convert_MP4_to_PNG(video_path):
    """
    - Args:
        - video_path (str)
    - Returns:
        - image_dir (str)
    """
    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    image_dir = os.path.join("../data/image", video_file_name_wo_ext)
    print("[INFO] Video Path      : {0}".format(video_path))
    print("[INFO] Image Directory : {0}".format(image_dir))

    if ((not os.path.exists(image_dir)) or get_args().start_over==True):
        print("[INFO] Start convert: mp4->png")
        save_all_frames(video_path=video_path, dir_path=image_dir, 
                        basename='img', ext='png', 
                        alpha=get_args().alpha, beta=get_args().beta)    
        print("[INFO] Finish convert: mp4->png")
    else:
        print("[INFO] Skip convert: mp4->png")

    return image_dir


def task_PNG_to_TXT(image_path, text_path):
    """
    - Args:
        - image_path (str)
        - text_path (str)
    - Returns:
    """
    make_AA(file_path=image_path, isOutText=True, out_path=text_path)


def tast_PNG_to_TXT_wrapper(args):
    return task_PNG_to_TXT(*args)


def convert_MP4_to_PNG_to_TXT(video_path):
    """
    - Args:
        - video_path (str)
    - Returns:
        - text_dir (str)
    """
    image_dir = convert_MP4_to_PNG(video_path)

    video_file_name_wo_ext = os.path.split(image_dir)[-1]
    image_flist = get_flist(image_dir, 'png')
    text_dir = os.path.join("../data/text", video_file_name_wo_ext)
    print("[INFO] Text Directory  : {0}".format(text_dir))
    if (not image_flist):
        print("[ERROR] Cannot find image files.")
        exit()

    if ((not os.path.exists(text_dir)) or get_args().start_over==True):
        print("[INFO] Start convert: png->txt")
        os.makedirs(text_dir, exist_ok=True)
        image_text_flist = []
        for image_path in image_flist:
            image_file_name = os.path.basename(image_path)
            image_file_name_wo_ext = os.path.splitext(image_file_name)[0]
            text_file_name = image_file_name_wo_ext + ".txt"
            text_path = os.path.join(text_dir, text_file_name)
            image_text_flist.append((image_path, text_path))
        # multiprocessing by Pool
        # used (Number of Logical CPUs - 1)
        pool = Pool(os.cpu_count() - 1)
        with tqdm(total=len(image_text_flist), bar_format=short_progress_bar) as t:
            for _ in pool.imap_unordered(tast_PNG_to_TXT_wrapper, image_text_flist):
                t.update(1)
        print("[INFO] Finish convert: png->txt")
    else:
        print("[INFO] Skip convert: png->txt")
    
    return text_dir


def convert_MP4_to_MP3(video_path):
    """
    - Args:
        - video_path (str)
    - Returns:
    """
    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    audio_dir = "../data/audio"
    audio_path = os.path.join("../data/audio", video_file_name_wo_ext+'.mp3')
    print("[INFO] Audio Path : {0}".format(audio_path))

    os.makedirs(audio_dir, exist_ok=True)

    if os.path.isfile(audio_path):
        print("[INFO] Skip convert MP4->MP3")
    else:
        print("[INFO] Start convert MP4->MP3")
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        print("[INFO] Finish convert MP4->MP3")

    return audio_path


def main():
    """
    - Args:
    - Returns:
    """
    pass


if __name__ == '__main__':
    main()
