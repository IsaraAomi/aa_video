import argparse

def get_args(video_path='../data/video/Shortcake_SONG_shorts_1080pFHR.mp4',
             start_over=False):
    """
    Get command line arguments.
    Arguments set the default values of command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--video-path", "-m", type=str, default=video_path)
    parser.add_argument("--start-over", "-s", action="store_true", default=start_over)

    return parser.parse_args()
