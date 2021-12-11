import cv2
import os
import sys


def save_all_frames(video_path, dir_path, basename, ext='png', alpha=1.0, beta=0.0):
    """
    - Args:
        - video_path (str)
        - dir_path (str)
        - basename (str)
        - ext (str)
        - alpha (float)
        - beta (float)
    - Returns:
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    n_all_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    digit = len(str(n_all_frames))

    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            if (alpha==1.0 and beta==0.0):
                frame_new = frame
            else:
                frame_new = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame_new)
            n += 1
            print('\r[INFO] {0}/{1}'.format(n, n_all_frames), end='')
        else:
            print('')
            return


def main():
    save_all_frames('../data/video/Shortcake_SONG_shorts_1080pFHR.mp4', \
                    '../data/image/Shortcake_SONG_shorts_1080pFHR', \
                    'img', 'png')


if __name__ == '__main__':
    main()
