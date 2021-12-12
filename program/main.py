import os, glob, re
import time
from tqdm import tqdm
from multiprocessing import Pool

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


def convert_MP4_to_PNG(video_path):
    """
    - Args:
        - video_path (str)
    - Returns:
    """
    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    image_dir = os.path.join("../data/image", video_file_name_wo_ext)
    print("[INFO] Video Path      : {0}".format(video_path))
    print("[INFO] Image Directory : {0}".format(image_dir))

    if ((not os.path.exists(image_dir)) or get_args().start_over==True):
        print("[INFO] Start convert: mp4->png")
        print("[INFO] Wait a moment")
        save_all_frames(video_path=video_path, dir_path=image_dir, 
                        basename='img', ext='png', 
                        alpha=get_args().alpha, beta=get_args().beta)    
        print("[INFO] Finish convert: mp4->png")
    else:
        print("[INFO] Skip convert: mp4->png")


# def convert_MP4_to_PNG_to_TXT_single(video_path):
#     """
#     - Args:
#         - video_path (str)
#     - Returns:
#     """
#     convert_MP4_to_PNG(video_path)

#     video_file_name = os.path.basename(video_path)
#     video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
#     image_dir = os.path.join("../data/image", video_file_name_wo_ext)
#     image_flist = get_image_flist(image_dir)
#     text_dir = os.path.join("../data/text", video_file_name_wo_ext)
#     print("[INFO] Text Directory  : {0}".format(text_dir))

#     if ((not os.path.exists(text_dir)) or get_args().start_over==True):
#         print("[INFO] Start convert: png->txt")
#         print("[INFO] Wait a moment")
#         os.makedirs(text_dir, exist_ok=True)
#         for image_path in tqdm(image_flist, bar_format=short_progress_bar):
#             image_file_name = os.path.basename(image_path)
#             image_file_name_wo_ext =  os.path.splitext(image_file_name)[0]
#             text_file_name = image_file_name_wo_ext + ".txt"
#             text_path = os.path.join(text_dir, text_file_name)
#             make_AA(file_path=image_path, isOutText=True, out_path=text_path)
#         print("[INFO] Finish convert: png->txt")
#     else:
#         print("[INFO] Skip convert: png->txt")


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


def convert_MP4_to_PNG_to_TXT_multi(video_path):
    """
    - Args:
        - video_path (str)
    - Returns:
    """
    convert_MP4_to_PNG(video_path)

    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    image_dir = os.path.join("../data/image", video_file_name_wo_ext)
    image_flist = get_image_flist(image_dir)
    text_dir = os.path.join("../data/text", video_file_name_wo_ext)
    print("[INFO] Text Directory  : {0}".format(text_dir))

    if ((not os.path.exists(text_dir)) or get_args().start_over==True):
        print("[INFO] Start convert: png->txt")
        print("[INFO] Wait a moment")
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
        pool = Pool(os.cpu_count()-1)
        with tqdm(total=len(image_text_flist), bar_format=short_progress_bar) as t:
            for _ in pool.imap_unordered(tast_PNG_to_TXT_wrapper, image_text_flist):
                t.update(1)
        print("[INFO] Finish convert: png->txt")
    else:
        print("[INFO] Skip convert: png->txt")


def show_video_on_console(video_path):
    """
    - Args:
        - video_path (str)
    - Returns:
    """
    # convert_MP4_to_PNG_to_TXT_single(video_path)
    convert_MP4_to_PNG_to_TXT_multi(video_path)

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

    # count down to start
    for i in range(3):
        print("\r[INFO] Start soon...: {0}".format(3-i), end="")
        time.sleep(1)

    # show
    for i, text_path in enumerate(text_flist):
        with open (text_path, mode='r') as f:
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
    show_video_on_console(video_path)
   
if __name__ == '__main__':
    main()
