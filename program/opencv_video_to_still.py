import cv2
import os


def save_all_frames(video_path, dir_path, basename, ext='jpg'):
    """
    - Args:
        - video_path (str)
        - dir_path (str)
        - basename (str)
        - ext (str)
    - Returns:
    """
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return

def main():
    save_all_frames('../data/video/Shortcake_SONG_shorts_1080pFHR.mp4', \
                    '../data/image/Shortcake_SONG_shorts_1080pFHR', \
                    'img', 'png')

if __name__ == '__main__':
    main()
