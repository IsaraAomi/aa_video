import time
import cv2
import pygame.mixer

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


def show_video_on_console(video_path, audio_path, with_audio=True):
    """
    - Args:
        - video_path (str)
        - audio_path (str)
        - with_audio (bool)
    - Returns:
    """
    text_dir = convert_MP4_to_PNG_to_TXT(video_path)
    text_flist = get_flist(text_dir, 'txt')

    # get text size
    text_path_0 = text_flist[0]
    width, height = get_text_size(text_path_0)
    print("[INFO] Image Size: (W, H)=({0}, {1})".format(width, height))
    cursor_move_up = ("\033[" + str(height+1) + "A")
    cursor_move_left = ("\033[" + str(width) + "D")

    # get fps of video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # count down to start
    for i in range(3):
        print("\r[INFO] Start soon...: {0}".format(3-i), end="")
        time.sleep(1)
    print('\r', end="")

    # play audio
    if with_audio:
        play_audio(audio_path)

    # show
    for i, text_path in enumerate(text_flist):
        with open (text_path, mode='r') as f:
            s = f.read()
            print(s + cursor_move_up + cursor_move_left)
        time.sleep(1.0/fps)


def main():
    """
    - Args:
    - Returns:
    """
    args = get_args()
    video_path = args.video_path
    with_audio = args.with_audio
    audio_path = convert_MP4_to_MP3(video_path)
    show_video_on_console(video_path, audio_path, with_audio)


if __name__ == '__main__':
    main()
