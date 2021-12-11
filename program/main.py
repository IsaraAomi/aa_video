import os, glob, re
import time
from tqdm import tqdm

from opencv_video_to_still import *
from AA import *
from args import *

# tqdm's bar_format
short_progress_bar="{l_bar}{bar:10}{r_bar}{bar:-10b}"

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def get_image_flist(dir):
    """
    - Args:
        - dir (str)
    - Returns:
        - flist (list)
    """
    flist = sorted(glob.glob(os.path.join(dir, '*.png')), key=natural_keys)
    return flist

def get_text_flist(dir):
    """
    - Args:
        - dir (str)
    - Returns:
        - flist (list)
    """
    flist = sorted(glob.glob(os.path.join(dir, '*.txt')), key=natural_keys)
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


def convert_MP4_to_PNG(video_path, start_over):
    """
    - Args:
        - video_path (str)
        - start_over (bool)
    - Returns:
    """
    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    image_dir = os.path.join("../data/image", video_file_name_wo_ext)
    
    print("[INFO] Video Path      : {0}".format(video_path))
    print("[INFO] Image Directory : {0}".format(image_dir))

    if ((not os.path.exists(image_dir)) or start_over==True):
        print("[INFO] Start convert: mp4->png")
        print("[INFO] Wait a moment")
        save_all_frames(video_path=video_path, dir_path=image_dir, basename='img', ext='png', alpha=1.2, beta=0.0)    
        print("[INFO] Finish convert: mp4->png")
    else:
        print("[INFO] Skip convert: mp4->png")

def convert_MP4_to_PNG_to_TXT(video_path, start_over):
    """
    - Args:
        - video_path (str)
        - start_over (bool)
    - Returns:
    """
    convert_MP4_to_PNG(video_path, start_over)

    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    image_dir = os.path.join("../data/image", video_file_name_wo_ext)
    image_flist = get_image_flist(image_dir)
    text_dir = os.path.join("../data/text", video_file_name_wo_ext)

    if ((not os.path.exists(text_dir)) or start_over==True):
        print("[INFO] Start convert: png->txt")
        print("[INFO] Wait a moment")
        os.makedirs(text_dir, exist_ok=True)
        for image_path in tqdm(image_flist, bar_format=short_progress_bar):
            image_file_name = os.path.basename(image_path)
            image_file_name_wo_ext =  os.path.splitext(image_file_name)[0]
            text_file_name = image_file_name_wo_ext + ".txt"
            text_path = os.path.join(text_dir, text_file_name)
            make_AA(file_path=image_path, isOutText=True, out_path=text_path)
        print("[INFO] Finish convert: png->txt")
    else:
        print("[INFO] Skip convert: png->txt")

def show_video_on_console(video_path, start_over):
    """
    - Args:
        - video_path (str)
        - start_over (bool)
    - Returns:
    """
    convert_MP4_to_PNG_to_TXT(video_path, start_over)

    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    text_dir = os.path.join("../data/text", video_file_name_wo_ext)
    text_flist = get_text_flist(text_dir)
    num_images = len(text_flist)

    # get text size
    text_path_0 = text_flist[0]
    width, height = get_text_size(text_path_0)
    print("[INFO] Image Size: (W, H)=({0}, {1})".format(width, height))
    cursor_move_up = ("\033[" + str(height+2) + "A")
    cursor_move_left = ("\033[" + str(width) + "D")

    for i, text_path in enumerate(text_flist):
        f = open(text_path, mode='r')
        s = f.read()
        print("[INFO] Image: {0}/{1}".format(i, num_images))
        print(s + cursor_move_up + cursor_move_left)
        time.sleep(1.0/60.0)

def main():
    """
    - Args:
    - Returns:
    """
    args = get_args()
    video_path = args.video_path
    start_over = args.start_over
    show_video_on_console(video_path, start_over)
   
if __name__ == '__main__':
    main()
