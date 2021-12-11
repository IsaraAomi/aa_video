import numpy as np
import os

from opencv_video_to_still import *
from AA import *
from args import *


def convert_MP4_to_PNG(video_path):
    """
    - Args:
    - Returns:
    """
    video_file_name = os.path.basename(video_path)
    video_file_name_wo_ext = os.path.splitext(video_file_name)[0]
    image_dir = os.path.join("../data/image", video_file_name_wo_ext)
    
    print("[INFO] Video Path      : {0}".format(video_path))
    print("[INFO] Image Directory : {0}".format(image_dir))

    if not os.path.exists(image_dir):
        print("[INFO] Start convert mp4 video to png images")
        print("[INFO] Wait a moment")
        save_all_frames(video_path=video_path, dir_path=image_dir, basename='img', ext='png')    
        print("[INFO] Finish convert process")
    else:
        print("[INFO] Skip convert process")


def main():
    """
    - Args:
    - Returns:
    """
    args = get_args()
    video_path = args.video_path

    convert_MP4_to_PNG(video_path)    




if __name__ == '__main__':
    main()
