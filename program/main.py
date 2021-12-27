from datetime import datetime
import time
import cv2
from numpy import int8
import pygame.mixer
from term_printer import ColorRGB, cprint

from args import *
from convert import *

def play_audio(audio_path):
    """
    - Args:
    - Returns:
    """
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(1)


def show_video_on_console(video_path, audio_path, audio_off=False, color=False):
    """
    - Args:
        - video_path (str)
        - audio_path (str)
        - audio_off (bool)
    - Returns:
    """
    text_dir, image_dir = convert_mp4_to_png_to_txt(video_path, width=50)
    text_flist = get_flist(text_dir, 'txt')
    image_flist = get_flist(image_dir, 'png')

    # get text size
    text_path = text_flist[0]
    t_width, t_height = get_text_size(text_path)
    print("[INFO] Text Image Size: (width, height)=({0}, {1})".format(t_width, t_height))
    cursor_move_up = ("\033[" + str(t_height+1) + "A")
    cursor_move_left = ("\033[" + str(t_width) + "D")

    # get video info
    v_width, v_height, frame, fps = get_video_info_by_cv2(video_path)
    print("[INFO] Video Info: (width, height, frame, fps)=({0}, {1}, {2})".format(v_width, v_height, frame, fps))

    # get video as numpy 4d array
    # (frame, t_height, t_width, num_color)
    if color:
        varray = get_4d_array(image_flist, t_width, t_height, frame)

    # count down to start
    for i in range(3):
        print("\r[INFO] Start soon...: {0}".format(3-i), end="")
        time.sleep(1)
    print('\r', end="")

    # play audio
    if not audio_off:
        play_audio(audio_path)

    # show
    if color:
        for i, image_path in enumerate(image_flist):
            t0 = time.time()
            imarray = varray[i,:,:,:]
            for idx_y in range(imarray.shape[0]):
                for idx_x in range(imarray.shape[1]):
                    r = imarray[idx_y,idx_x,0]
                    g = imarray[idx_y,idx_x,1]
                    b = imarray[idx_y,idx_x,2]
                    cprint(" ", attrs=[ColorRGB(r, g, b, is_bg=True)], end="")
                print()
            print(cursor_move_up + cursor_move_left)
            i += 1
            t_add = 1.0/fps - (time.time() - t0)
            if t_add >= 0:
                time.sleep(t_add)
            else:
                # print("[WARNING] Play speed is under {0} fps".format(fps))
                pass
    else:
        for text_path in text_flist:
            t0 = time.time()
            with open (text_path, mode='r') as f:
                s = f.read()
                print(s + cursor_move_up + cursor_move_left)
            t_add = 1.0/fps - (time.time() - t0)
            if t_add >= 0:
                time.sleep(t_add)
            else:
                # print("[WARNING] Play speed is under {0} fps".format(fps))
                pass


def main():
    """
    - Args:
    - Returns:
    """
    # STEP = 8

    # for r in reversed(range(0, 256, STEP)):
    #     b = 255 - r
    #     for g in range(0, 256, STEP):           
            # cprint(" " * 4, attrs=[ColorRGB(r, g, b, is_bg=True)], end="")

    args = get_args()
    video_path = args.video_path
    audio_off = args.audio_off
    color = args.color
    audio_path = convert_mp4_to_mp3(video_path)
    show_video_on_console(video_path, audio_path, audio_off, color)


if __name__ == '__main__':
    main()
